"""
changes need to be done:
1. add to bases field that state if there are available drones in this storge (i called this field is_available),
   we probably will have to add also a way of communication between bases and our system
2. add to drones field that state if the drone is ready for delivery, useful when trying to allocate drone to delivery
   and not sure if the drone is fine/has enough battery/etc.., i called this field ready_for_delivery,
   this will also use the communication from point 1
   we also need to add planned start time for drone to start the path
3. change delivery table to contain time of request
4. add is_collected, is_delivered to delivery db
5. add id to steps because step_id cant be primary it may have same value for different drones
6. change edr - for each drone only one delivery and the opposite

way of thinking:
1. in order to decrease the error measurements of the gps in the next version the program should give the mean value
   of the location the gps returned in the time that passed. for example: now we update the DB every half a sec
   and in this time 20 Hz gps can sample 10 times the location, so the mean of this samplings can give us a pretty
   accurate location. maybe there is a gps component that already does this and can be put on the drone?
2. the drones will send the step id of their current step to the manager, clear their steps at end of rout

questions:
1. we will need to raise the base area weight as obstacle so that we can jus raise the drone to the matching height
   according to its direction of moving, and keep it in its height limits, we may also need to create few
   landing/takeoff points for each base, should the landing/takeoff need separate functionality? maybe we will leave
   it blank for now, it can also be done using lasers tech and so.

next steps:
1. fix error to be total of 2.64 and not for each axis
"""
import random

import numpy as np

import shared
from shared import *
from rrt_star_functions import RRTStar
import math
import mysql.connector
# from manager import *
# from temp import visualize_map_at_time


def check_db_for_new_deliveries(conn):
    query = "SELECT * FROM deliveries WHERE drone_id IS NULL ORDER BY requested_date LIMIT 1"
    result = query_db(conn, query)
    if result:
        return Delivery(*result[0])
    return None


def check_db_for_collected_deliveries(conn):
    query = ("SELECT * FROM deliveries WHERE is_collected = TRUE AND is_delivered = FALSE ORDER BY requested_date")
    result = query_db(conn, query)
    if result:
        deliveries = [Delivery(*delivery) for delivery in result]
        for delivery in deliveries:
            drone = get_drone_by_id(conn, delivery.drone_id)
            if drone.planned_start_time is None:
                return delivery
    return None


def check_db_for_delivered_deliveries(conn):
    query = ("SELECT * FROM deliveries WHERE is_collected = TRUE AND is_delivered = TRUE ORDER BY requested_date")
    result = query_db(conn, query)
    if result:
        deliveries = [Delivery(*delivery) for delivery in result]
        for delivery in deliveries:
            drone = get_drone_by_id(conn, delivery.drone_id)
            if drone.planned_start_time is None:
                return delivery
    return None


def get_nearest_base(conn, x, y):
    query = "SELECT * FROM bases WHERE is_available = TRUE"
    bases = query_db(conn, query)
    base_objects = [Base(*base) for base in bases]

    nearest_base = None
    min_base_to_location_dis = float('inf')

    for base in base_objects:
        base_to_location_dis = distance(base.x, base.y, x, y)
        if base_to_location_dis < min_base_to_location_dis:
            nearest_base = base
            min_base_to_location_dis = base_to_location_dis
    return nearest_base


def allocate_drone(conn, delivery, pickup_location):
    # allocating drone based on proximity from the pickup location, available drones in the storages
    nearest_base = get_nearest_base(conn, pickup_location.x, pickup_location.y)

    if nearest_base is not None:
        query = f"SELECT * FROM drones WHERE base_id = {nearest_base.base_id} AND ready_for_delivery = TRUE LIMIT 1"
        result = query_db(conn, query)
        if not result:
            print("No drones in the nearest base that is available")
            return None
        chosen_drone = Drone(*result[0])
        if chosen_drone:
            query = (f"UPDATE deliveries SET drone_id = {chosen_drone.drone_id} WHERE "
                     f"delivery_id = {delivery.delivery_id}")
            query_db(conn, query)
        return chosen_drone
    return None


def get_drone_by_id(conn, drone_id):
    query = f"SELECT * FROM drones WHERE drone_id = {drone_id}"
    result = query_db(conn, query)
    return Drone(*result[0])


def get_pickup_location(conn, delivery):
    query = (f"SELECT pickup_id, pickup_x_coordinate as x, pickup_y_coordinate as y FROM pickup_locations "
             f"WHERE pickup_id = {delivery.pickup_id}")
    result = query_db(conn, query)
    pickup_location = DroneStopLocation(*result[0])
    if pickup_location:
        return pickup_location
    return None


def get_drop_location(conn, delivery):
    query = (f"SELECT drop_id, drop_x_coordinate as x, drop_y_coordinate as y FROM drop_locations "
             f"WHERE drop_id = {delivery.drop_id}")
    result = query_db(conn, query)
    drop_location = DroneStopLocation(*result[0])
    if drop_location:
        return drop_location
    return None


def send_steps_to_drone(conn, drone_id, steps, planned_start_time):
    for index, step in enumerate(steps):
        x, y, z, t = step

        # Insert step into steps table
        query = (
            f"INSERT INTO steps (step_index, drone_x_coordinate, drone_y_coordinate, drone_z_coordinate, drone_id)"
            f" VALUES ({index}, {x}, {y}, {z}, {drone_id})")
        query_db(conn, query)

        # Add cubic obstacle to obstacles table
        obstacle_start_time = t - 0.5
        obstacle_end_time = t + 0.5

        # Calculate bounding box for the sphere
        query = (f"INSERT INTO obstacles (x_min, x_max, y_min, y_max, z_min, z_max, t_start, t_end, value)"
                 f" VALUES ({round(x - shared.SAFE_CUBE_RADIUS, 2)}, {round(x + shared.SAFE_CUBE_RADIUS, 2)}, "
                 f"{round(y - shared.SAFE_CUBE_RADIUS, 2)}, {round(y + shared.SAFE_CUBE_RADIUS, 2)}, "
                 f"{round(z - shared.SAFE_CUBE_RADIUS, 2)}, {round(z + shared.SAFE_CUBE_RADIUS, 2)}, "
                 f"{round(obstacle_start_time, 2)}, {round(obstacle_end_time, 2)}, {shared.OBSTACLE_WEIGHT})")
        query_db(conn, query)

    query = (f"UPDATE drones SET base_id = NULL, ready_for_delivery = NULL, planned_start_time = {planned_start_time} "
             f"WHERE drone_id = {drone_id}")
    query_db(conn, query)


def distance(first_location_x, first_location_y, second_location_x, second_location_y):
    return math.sqrt((second_location_x - first_location_x) ** 2 + (second_location_y - first_location_y) ** 2)


def get_random_height():
    return random.randint(shared.MIN_HEIGHT_FLIGHT, shared.MAX_HEIGHT_FLIGHT)

def sql_conn():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Aa123456789!",
            database="final_project"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def process_path(conn, drone, start, goal, message):
    rrt_star = RRTStar(start, goal, conn, max_iter=RRT_ITERATIONS)
    path = rrt_star.find_path()
    if path:
        print(f"Path found! for {message}")
        send_steps_to_drone(conn, drone.drone_id, path, start[shared.LOCATION_INDEX_FOR_T])
    else:
        print(f"No path found for {message}")
        return False
    return True


def main():
    conn = sql_conn()
    if conn is None:
        print("Failed to connect to the database.")
        return
    #obstacle_map = np.load('4d_obstacle_map.npy')
    system_status = True
    # visualize_map_at_time(0, obstacle_map)
    try:
        while system_status:
            new_delivery = new_delivery = check_db_for_new_deliveries(conn)
            if new_delivery:
                pickup_location = get_pickup_location(conn, new_delivery)
                if pickup_location is None:
                    print("Couldn't find delivery pickup point, something wrong.")
                    system_status = False
                    continue
                drone = allocate_drone(conn, new_delivery, pickup_location)
                if drone is None:
                    print("There are no available drones.")
                    system_status = False
                    continue
                planned_start_time = time.time() + shared.WAIT_TIME_FOR_DELIVERY
                start = [drone.false_x_coord, drone.false_y_coord, drone.false_z_coord + get_random_height(), planned_start_time]
                goal = [pickup_location.x, pickup_location.y, get_random_height(), math.inf]
                process_path(conn, drone, start, goal, "new delivery")

            collected_delivery = check_db_for_collected_deliveries(conn)
            if collected_delivery:
                drop_location = get_drop_location(conn, collected_delivery)
                if drop_location is None:
                    print("Couldn't find delivery drop point, something wrong.")
                    system_status = False
                    continue
                drone = get_drone_by_id(conn, collected_delivery.drone_id)
                if drone is None:
                    print("Couldn't find delivery drone, something wrong.")
                    system_status = False
                    continue
                planned_start_time = time.time() + shared.WAIT_TIME_FOR_DELIVERY
                start = [drone.false_x_coord, drone.false_y_coord, drone.false_z_coord + get_random_height(), planned_start_time]
                goal = [drop_location.x, drop_location.y, get_random_height(), math.inf]
                process_path(conn, drone, start, goal, "drop point")

            delivered_delivery = check_db_for_delivered_deliveries(conn)
            if delivered_delivery:
                drone = get_drone_by_id(conn, delivered_delivery.drone_id)
                if drone is None:
                    print("Couldn't find delivery drone, something wrong.")
                    system_status = False
                    continue
                return_base = get_nearest_base(conn, drone.false_x_coord, drone.false_y_coord)
                planned_start_time = time.time() + shared.WAIT_TIME_FOR_DELIVERY
                start = [drone.false_x_coord, drone.false_y_coord, drone.false_z_coord + get_random_height(), planned_start_time]
                goal = [return_base.x, return_base.y, get_random_height(), math.inf]
                process_path(conn, drone, start, goal, "return to base")
    finally:
        conn.close()


if __name__ == '__main__':
    main()