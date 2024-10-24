import multiprocessing
from multiprocessing import Manager
import mysql.connector
import random
import time
import numpy as np

import shared
from shared import *


# this page act both as the reality generator and the db handler


def create_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Aa123456789!",
            database="final_project"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error creating connection: {err}")
        return None


def query_db(conn, query):
    cursor = conn.cursor(buffered=False)
    try:
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        conn.rollback()
    finally:
        conn.commit()
        cursor.close()
    return None


def add_random_delivery(conn):
    current_time = time.time()

    # Check if 2 seconds have passed since the last delivery
    if current_time - shared.LAST_DELIVERY_TIME < shared.DELIVERY_GAPS:
        return  # Not enough time has passed, so don't add a delivery

    # Update the last delivery time
    shared.LAST_DELIVERY_TIME = current_time

    # Get all pickup IDs
    pickup_query = "SELECT pickup_id FROM pickup_locations"
    pickup_results = query_db(conn, pickup_query)
    pickup_ids = [result[0] for result in pickup_results]

    # Get all drop IDs
    drop_query = "SELECT drop_id FROM drop_locations"
    drop_results = query_db(conn, drop_query)
    drop_ids = [result[0] for result in drop_results]

    # Randomly select IDs
    random_pickup_id = random.choice(pickup_ids)
    random_drop_id = random.choice(drop_ids)

    # Insert new delivery
    query = (f"INSERT INTO deliveries (drone_id, drop_id, pickup_id, is_collected, is_delivered, requested_date) VALUES"
             f" (NULL, {random_drop_id}, {random_pickup_id}, FALSE, FALSE, {time.time()})")
    query_db(conn, query)


def drone_stopped(conn, drone, stop_location):
    query = f"DELETE FROM steps WHERE drone_id = {drone.drone_id}"
    query_db(conn, query)
    query = ("UPDATE drones SET velocity = 0, planned_start_time = NULL, step_index = NULL, ready_for_delivery = TRUE, "
             f"drone_x_coordinate = {stop_location.x}, drone_y_coordinate = {stop_location.y}, drone_z_coordinate = 0, "
             f"real_x = {stop_location.x}, real_y = {stop_location.y}, real_z = 0, is_fault = 0, last_moved = 0 "
             f"WHERE drone_id = {drone.drone_id}")
    query_db(conn, query)
    drone.velocity = 0
    drone.planned_start_time = None
    drone.step_index = None
    drone.ready_for_delivery = True


def delivery_check_collected_and_set(conn, delivery, drone, last_step):
    if delivery.drop_id is not None and not delivery.is_collected:
        query = f"UPDATE deliveries SET is_collected = TRUE WHERE delivery_id = {delivery.delivery_id}"
        query_db(conn, query)
        delivery.is_collected = True
        query = f"UPDATE drones SET is_package_load = TRUE WHERE drone_id = {delivery.drone_id}"
        query_db(conn, query)
        drone.is_package_load = True
        drone_stopped(conn, drone, last_step)
        return True
    return False


def delivery_check_delivered_and_set(conn, delivery, drone, last_step):
    if delivery.drop_id is not None and delivery.is_collected and not delivery.is_delivered:
        query = f"UPDATE deliveries SET is_delivered = TRUE WHERE delivery_id = {delivery.delivery_id}"
        query_db(conn, query)
        delivery.is_delivered = True
        query = f"UPDATE drones SET is_package_unload = TRUE WHERE drone_id = {drone.drone_id}"
        query_db(conn, query)
        drone.is_package_unload = True
        drone_stopped(conn, drone, last_step)
        return True
    return False


def delivery_check_finish_and_set(conn, delivery, drone, last_step):
    if delivery.drop_id is not None and delivery.is_collected and delivery.is_delivered:
        query = (f"SELECT * FROM bases WHERE ROUND(base_x_coordinate, 1) = {last_step.x} AND "
                 f"ROUND(base_y_coordinate, 1) = {last_step.y}")
        result = query_db(conn, query)
        base = Base(*result[0])
        query = (f"UPDATE drones SET is_package_load = FALSE, is_package_unload = FALSE, base_id = {base.base_id} "
                 f"WHERE drone_id = {drone.drone_id}")
        query_db(conn, query)
        drone_stopped(conn, drone, last_step)
        query = f"UPDATE drones SET drone_z_coordinate = -1, real_z = -1 WHERE drone_id = {drone.drone_id}"
        query_db(conn, query)
        query = f"DELETE FROM deliveries WHERE delivery_id = {delivery.delivery_id}"
        query_db(conn, query)
        return True
    return False


def reset_db(conn):
    query = "DELETE FROM obstacles WHERE t_start != 0"
    query_db(conn, query)
    query = "TRUNCATE TABLE deliveries"
    query_db(conn, query)
    query = "TRUNCATE TABLE logs"
    query_db(conn, query)
    query = "TRUNCATE TABLE steps"
    query_db(conn, query)
    query = f"UPDATE drones SET drone_z_coordinate = -1, real_z = -1"
    query_db(conn, query)
    query = ("SELECT * FROM drones WHERE is_fault = TRUE OR velocity != 0 OR is_package_load = TRUE OR "
             "is_package_unload = TRUE OR step_index IS NOT NULL OR ready_for_delivery = FALSE OR base_id is NULL "
             "OR planned_start_time IS NOT NULL OR last_moved != 0 OR last_communication != 0")
    result = query_db(conn, query)
    if result is not None:
        drones_to_reset = [Drone(*drone) for drone in result]
        query = "SELECT * FROM bases"
        result = query_db(conn, query)
        bases = [Base(*base) for base in result]
        for drone in drones_to_reset:
            base_index = drone.drone_id % len(bases)
            query = (f"UPDATE drones SET is_fault = FALSE, velocity = 0, "
                     f"drone_x_coordinate = {bases[base_index].x}, drone_y_coordinate = {bases[base_index].y}, "
                     f"real_x = {bases[base_index].x}, real_y = {bases[base_index].y}, is_detouring = 0,"
                     f"is_package_load = FALSE, is_package_unload = FALSE, step_index = NULL, last_communication = 0, "
                     f"planned_start_time = NULL, base_id = {bases[base_index].base_id}, ready_for_delivery = TRUE, "
                     f"last_moved = 0 WHERE drone_id = {drone.drone_id}")
            query_db(conn, query)


def update_drone_location(conn, drone, steps):
    time_pass_from_last_move = time.time() - drone.last_moved
    if time_pass_from_last_move < GPS_SAMPLE_SPEED:
        return
    real_location = np.array([drone.real_x_coord, drone.real_y_coord, drone.real_z_coord])
    false_location = np.array([drone.false_x_coord, drone.false_y_coord, drone.false_z_coord])
    direction = (np.array([steps[drone.step_index + 1].x, steps[drone.step_index + 1].y, steps[drone.step_index + 1].z])
                 - false_location)
    direction_norm = np.linalg.norm(direction)
    distance_to_move = FLIGHT_VELOCITY * time_pass_from_last_move
    movement_vector = (direction / direction_norm) * distance_to_move
    new_position = real_location + movement_vector
    drone.real_x_coord = new_position[shared.LOCATION_INDEX_FOR_X]
    drone.real_y_coord = new_position[shared.LOCATION_INDEX_FOR_Y]
    drone.real_z_coord = new_position[shared.LOCATION_INDEX_FOR_Z]
    error = np.random.normal(0, MEAN_POSITIONING_ERROR, size=3)
    false_location = new_position + error
    drone.false_x_coord = false_location[shared.LOCATION_INDEX_FOR_X]
    drone.false_y_coord = false_location[shared.LOCATION_INDEX_FOR_Y]
    drone.false_z_coord = false_location[shared.LOCATION_INDEX_FOR_Z]
    drone.last_moved = time.time()
    query = (f"UPDATE drones SET last_moved = {drone.last_moved}, drone_x_coordinate = {drone.false_x_coord}, "
             f"drone_y_coordinate = {drone.false_y_coord}, drone_z_coordinate = {drone.false_z_coord}, "
             f"real_x = {drone.real_x_coord}, real_y = {drone.real_y_coord}, real_z = {drone.real_z_coord} "
             f"WHERE drone_id = {drone.drone_id}")
    query_db(conn, query)
    false_location_next_step_distance = np.linalg.norm(false_location - np.array([steps[drone.step_index + 1].x,
                                                                                  steps[drone.step_index + 1].y,
                                                                                  steps[drone.step_index + 1].z]))
    if false_location_next_step_distance < shared.trustable_range:
        drone.step_index += 1
        query = f"UPDATE drones SET step_index = {drone.step_index} WHERE drone_id = {drone.drone_id}"
        query_db(conn, query)


def process_delivery(args):
    shared_namespace, delivery = args

    query = f"SELECT * FROM drones WHERE drone_id = {delivery.drone_id}"
    result = query_db(conn, query)
    connected_drone = Drone(*result[0])

    if connected_drone.step_index is None:
        # means that drone waiting at base/pickup point/drop point
        if (connected_drone.planned_start_time and time.time() >= connected_drone.planned_start_time and
                connected_drone.step_index is None):
            real_location = np.array([connected_drone.real_x_coord, connected_drone.real_y_coord, TEMP_HEIGHT])
            error = np.random.normal(0, MEAN_POSITIONING_ERROR, size=3)
            false_location = real_location + error
            query = (f"UPDATE drones SET real_z = {real_location[shared.LOCATION_INDEX_FOR_Z]}, step_index = 0, "
                     f"drone_x_coordinate = {false_location[shared.LOCATION_INDEX_FOR_X]}, "
                     f"drone_y_coordinate = {false_location[shared.LOCATION_INDEX_FOR_Y]}, "
                     f"drone_z_coordinate = {false_location[shared.LOCATION_INDEX_FOR_Z]}, "
                     f"velocity = {shared.FLIGHT_VELOCITY}, last_moved = {connected_drone.planned_start_time} "
                     f"WHERE drone_id = {connected_drone.drone_id}")
            query_db(conn, query)
            connected_drone.real_z_coord = real_location[shared.LOCATION_INDEX_FOR_Z]
            connected_drone.step_index = 0
            connected_drone.false_x_coord = false_location[shared.LOCATION_INDEX_FOR_X]
            connected_drone.false_y_coord = false_location[shared.LOCATION_INDEX_FOR_Y]
            connected_drone.false_z_coord = false_location[shared.LOCATION_INDEX_FOR_Z]
            connected_drone.last_moved = connected_drone.planned_start_time
        else:
            return

    # this drone is in the air
    query = f"SELECT * FROM steps WHERE drone_id = {connected_drone.drone_id} order by step_index"
    result = query_db(conn, query)
    if not result:
        print("No steps for active drone, something is wrong")
        return

    drone_steps = [Step(*step) for step in result]
    update_drone_location(conn, connected_drone, drone_steps)
    query = f"SELECT * FROM steps WHERE drone_id = {connected_drone.drone_id} ORDER BY step_index DESC LIMIT 1"
    result = query_db(conn, query)
    if not result:
        print("Cant get last step, something is wrong")
        return
    last_step = Step(*result[0])
    if last_step.step_index == connected_drone.step_index:
        # this drone finished its path
        if not delivery_check_collected_and_set(conn, delivery, connected_drone, last_step):
            if not delivery_check_delivered_and_set(conn, delivery, connected_drone, last_step):
                if not delivery_check_finish_and_set(conn, delivery, connected_drone, last_step):
                    print("Something is wrong.")


def worker_init(shared_namespace):
    global conn
    conn = create_connection()
    if conn is None:
        print("Failed to create database connection in worker process.")


def main():
    manager = Manager()
    shared_namespace = manager.Namespace()

    try:
        # Create a pool of worker processes
        pool = multiprocessing.Pool(initializer=worker_init, initargs=(shared_namespace,))

        # Create a separate connection for the main process
        main_conn = create_connection()
        if main_conn is None:
            print("Failed to create database connection in main process. Exiting.")
            return

        reset_db(main_conn)

        while True:
            add_random_delivery(main_conn)
            query = "SELECT * FROM deliveries WHERE drone_id IS NOT NULL"
            result = query_db(main_conn, query)
            active_deliveries = [Delivery(*delivery) for delivery in result]

            # Map the processing function to all active deliveries in parallel
            pool.map(process_delivery, [(shared_namespace, delivery) for delivery in active_deliveries])

            # Add a small delay to prevent tight looping
            time.sleep(0.05)
    except Exception as e:
        print(f"An error occurred in main: {e}")
    finally:
        if main_conn:
            main_conn.close()
        pool.close()
        pool.join()


if __name__ == '__main__':
    main()