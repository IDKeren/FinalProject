import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Use an interactive backend for live plotting

# Constants for the detour algorithm
MAX_VELOCITY = 10  # Maximum velocity (example value)
SAFE_RADIUS = 10  # Safe radius for each drone
SAFE_RADIUS_FROM_OBSTACLES = 7
COLLISION_RADIUS = 2.63 # High collision potential radius
ANG_RATE = 150  # Angular rate in degrees per second for commercial drones acroding to the article
DRONE_DETECTION_DIAMETER = 20  # Detection radius of each drone

# Global variables to keep track of the plot and axes
fig, ax = None, None

def create_database_connection(host_name, user_name, user_password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        if connection.is_connected():
            log_to_db(connection,-1, "System: INFO", "MySQL Database connection successful")
            return connection
    except Error as e:
        print(f"Connection error: '{e}'")
        return None

def log_to_db(connection, drone_id, log_level, log_message):
    """
    Log a message to the database.
    """
    log_query = """
    INSERT INTO logs (drone_id, log_message, log_level)
    VALUES (%s, %s, %s)
    """
    data = (drone_id, log_message, log_level)
    execute_write_query(connection, log_query, data)

def execute_read_query(connection, query):
    
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        log_to_db(connection, -1, "System: WARNING", f"Read query error: '{e}'")
    except Exception as ex:
        log_to_db(connection, -1, "System: ERROR", f"Unexpected error: {ex}")
        return []
    finally:
        connection.commit()
        cursor.close()

def execute_write_query(connection, query, data):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        connection.commit()
        cursor.close()

def angle_between(v1, v2):
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0  # If either vector is zero, angle is 0
    cos_theta = np.dot(v1, v2) / (norm_v1 * norm_v2)
    angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    return np.degrees(angle)

def single_drone(drone, obstacle, maxV, safeR, angRate, detectionR, connection, detour_source, distance):
    """
    Execute the single drone detour algorithm.
    """
    velocity = maxV
    # Fetch detouring status from the drone dictionary

    if drone['is_detouring'] == 0 : 
            # Continue with detour logic if an alert is raised
            vlos = np.array(obstacle['position']) - np.array(drone['position'])
            unit_vector = vlos / distance
            if detour_source == "obstacle":
                log_to_db(connection, drone['id'], "WARNING",
                            f"Alert: Drone {drone['id']} with cordinates {drone['position']} is too close! to obstacle {obstacle['id']} Distance is lower than {SAFE_RADIUS} meters")  # Log the alert message
                Vod = np.array(drone['velocity'])
            else:
                log_to_db(connection, drone['id'], "WARNING",
                            f"Alert: Drone {drone['id']} with cordinates {drone['position']} is too close! to drone {obstacle['id']} Distance is {distance} meters")
                Vod = np.array(obstacle['velocity']) - np.array(drone['velocity'])
            angle_gamma = angle_between(Vod, vlos)

            # Check if the drone is within the safe radius of the obstacle
            #print(f"angle_gamma: {angle_gamma}")
            if detour_source == "obstacle" and drone['is_detouring'] == 0:
                
                    detour_steps = calculate_detour_steps(drone, obstacle, safeR)
                    insert_detour_steps(connection, drone, detour_steps)
                    
                    drone['is_detouring'] = 2
                    log_to_db(connection, drone['id'], "System: INFO",
                        f"Drone {drone['id']} is detouring to avoid collision with {detour_source} {obstacle['id']}")

            elif( distance < DRONE_DETECTION_DIAMETER):
                    # Update drone status to detouring and reduce speed
                    velocity = maxV / 2
                    detour_steps = calculate_dynamic_detour_steps(drone, obstacle, vlos, Vod, angle_gamma, safeR)
                    insert_detour_steps(connection, drone, detour_steps)
                    drone['is_detouring'] = 1
                    log_to_db(connection, drone['id'], "System: INFO", f"Drone {drone['id']} is detouring to avoid collision with {detour_source} {obstacle['id']}")
    terminate_detour(drone, maxV, connection)

def calculate_dynamic_detour_steps(drone, obstacle, vlos, Vod, angle_gamma, safeR):
    """
    Calculate detour steps for the drone based on vlos, Vod, and angle_gamma.
    This function dynamically generates steps to avoid collisions.
    """
    # Normalize the line of sight vector
    vlos_norm = vlos / np.linalg.norm(vlos)

    # Calculate a detour direction perpendicular to the line of sight vector
    detour_direction = np.cross(vlos_norm, np.array([0, 0, 1]))  # Cross product to find perpendicular direction
    detour_direction = detour_direction / np.linalg.norm(detour_direction)  # Normalize

    # Adjust detour direction based on the relative velocity and angle
    if np.all(angle_gamma) > 0:
        detour_direction = np.cross(detour_direction, vlos_norm)  # Adjust direction based on relative velocity
        detour_direction = detour_direction / np.linalg.norm(detour_direction)

    # Scale detour direction by the safe radius to move the drone away
    detour_distance = safeR/2
    step1 = np.array(drone['position']) + detour_direction * detour_distance
    step2 = step1 + detour_direction * detour_distance


    # Define detour steps as tuples with step index and coordinates
    detour_steps = [
        (1, step1[0], step1[1], step1[2], drone['id']),
        (2, step2[0], step2[1], step2[2], drone['id'])
    ]

    return detour_steps

def calculate_detour_steps(drone, obstacle, safeR):
    """
    Calculate the detour steps for the drone.
    """
    drone_pos = np.array(drone['position'])
    obstacle_pos = np.array(obstacle['position'])
    direction = (drone_pos - obstacle_pos) / np.linalg.norm(drone_pos - obstacle_pos)

    # Example detour steps: move in the opposite direction of the obstacle to avoid it
    detour_distance = safeR + 1
    step1 = drone_pos + direction * detour_distance
    step2 = step1 + direction * detour_distance


    detour_steps = [
        (1, step1[0], step1[1], step1[2], drone['id']),
        (2, step2[0], step2[1], step2[2], drone['id'])

    ]
    return detour_steps

def update_drone_detour_status(connection, drone_id, is_detouring):
    """
    Update the detouring status of a drone in the database.
    """
    update_query = """
    UPDATE drones 
    SET is_detouring = %s
    WHERE drone_id = %s
    """
    execute_write_query(connection, update_query, (is_detouring, drone_id))

def insert_detour_steps(connection, drone, detour_steps):
    """
    Insert detour steps into the steps table starting from the current step index,
    and update subsequent steps' indexes accordingly.
    """
    try:
        current_step = drone['step_index']
        expected_detouring_step = current_step + len(detour_steps)
        update_drone_detour_status(connection, drone['id'], expected_detouring_step)

        if current_step is not None:
            # Use the current step index as the starting point for the new detour steps
            current_step_index = current_step
            next_index = current_step_index + 1
            # Step 2: Update subsequent steps to make space for new detour steps
            step_increase = len(detour_steps)  # Number of detour steps being inserted
            update_steps_query = """
            UPDATE steps
            SET step_index = step_index + %s
            WHERE drone_id = %s AND step_index >= %s
            """
            execute_write_query(connection, update_steps_query, (step_increase, drone['id'], next_index))

            # Step 3: Insert detour steps starting from the current step index
            insert_query = """
            INSERT INTO steps (step_index, drone_x_coordinate, drone_y_coordinate, drone_z_coordinate, drone_id)
            VALUES (%s , %s, %s, %s, %s)
            """

            # Adjust the step indices of the detour steps to start from the current index
            adjusted_detour_steps = [
                (current_step_index + i+1, step[1], step[2], step[3], drone['id'])  # Update step_index and keep other values
                for i, step in enumerate(detour_steps)
                ]

            # Insert the adjusted detour steps into the database
            for step in adjusted_detour_steps:
                execute_write_query(connection, insert_query, step) 

            # Step 4: Update the drone's step_index to the current step index
            update_drone_query = """
                UPDATE drones
                SET step_index = %s
                WHERE drone_id = %s
                """
            # Update to the new step index (e.g., first detour step index)

            execute_write_query(connection, update_drone_query, (current_step_index, drone['id']))

            log_to_db(connection, drone['id'], "INFO", f"Inserted detour steps for Drone {drone['id']} starting from index {current_step_index}.")
            print(f"Inserted detour steps for Drone {drone['id']} starting from index {current_step_index}.")

        else:
            log_to_db(connection, drone['id'], "WARNING", f"No current step found for Drone {drone['id']}. Unable to insert detour steps.")
            print(f"No current step found for Drone {drone['id']}. Unable to insert detour steps.")

    except Exception as e:
        log_to_db(connection, drone['id'], "ERROR", f"Error inserting detour steps for Drone {drone['id']}: {e}")
        print(f"Error inserting detour steps for Drone {drone['id']}: {e}")


def terminate_detour(drone, initialVel, connection):
    """
    Terminate the detour when the drone's detouring step index matches the step_index.
    """
    # Check if the query returned any results, indicating detouring should terminate
    if drone['is_detouring'] == drone['step_index']:
        # Reset detouring status and detouring step index
        update_drone_detour_status(connection, drone['id'], 0)
        drone['is_detouring'] = 0
        drone['velocity'] = initialVel
        log_to_db(connection, drone['id'], "INFO", f"Drone {drone['id']} has terminated the detour.")

def fetch_latest_positions(connection):
    query = """
    SELECT s.drone_id, s.drone_x_coordinate, s.drone_y_coordinate, s.drone_z_coordinate, d.velocity
    FROM steps s
    INNER JOIN (
        SELECT drone_id, MAX(step_index) AS latest_step
        FROM steps
        GROUP BY drone_id
    ) latest_steps ON s.drone_id = latest_steps.drone_id AND s.step_index = latest_steps.latest_step
    INNER JOIN drones d ON s.drone_id = d.drone_id;
    """
    return execute_read_query(connection, query)

def fetch_current_positions(connection):
    # Query to get current positions from the drones table
    query = """
        SELECT drone_id, drone_x_coordinate, drone_y_coordinate, drone_z_coordinate, velocity, is_detouring, step_index 
        FROM drones
        where drone_z_coordinate > 0;
        """
    return execute_read_query(connection, query)

def fetch_active_obstacles(connection):
    """
    Fetch active obstacles from the database within the current time frame.
    """
    query = f"""
    SELECT id, x_min, x_max, y_min, y_max, z_min, z_max
    FROM permanent_obstacles
    """
    return execute_read_query(connection, query)



def fault(connection, drone_id1, drone_id2):

    update_drone_query = """
                                UPDATE drones
                                SET is_fault = %s
                                WHERE drone_id = %s
                                """
    # Update to the new step index (e.g., first detour step index)

    execute_write_query(connection, update_drone_query,  (1, drone_id1))
    execute_write_query(connection, update_drone_query,  (1, drone_id1))

def generate_obstacles(connection):
    obstacles = fetch_active_obstacles(connection)
    obstacles_list = []
    for obstacle in obstacles:
        obstacle_position = [
            (obstacle[1] + obstacle[2]) / 2,  # X position (center of x_min and x_max)
            (obstacle[3] + obstacle[4]) / 2,  # Y position (center of y_min and y_max)
            (obstacle[5] + obstacle[6]) / 2  # Z position (center of z_min and z_max)
        ]

        obstacles_list.append({
            'id': obstacle[0],
            'position': obstacle_position,  # Center position in 3D space
            'x_min': obstacle[1],
            'x_max': obstacle[2],
            'y_min': obstacle[3],
            'y_max': obstacle[4],
            'z_min': obstacle[5],
            'z_max': obstacle[6],
        })
    return obstacles_list

def check_drones_for_collisions(connection,drones,obstacles):
    if connection is None:
        log_to_db(connection, -1, "System: ERROR", "No connection to the database.")
        return
    
    # Convert to a list of dictionaries for easier handling
    drone_list = []
    for drone in drones:
        drone_list.append({
            'id': drone[0],
            'position': [drone[1], drone[2], drone[3]],
            'velocity': [drone[4], drone[4], drone[4]],  # Simplified for example; adjust as needed
            'is_detouring': drone[5],
            'step_index': drone[6]
        })

        # Check each drone against only nearby drones and exclude ground drones
        for i, drone in enumerate(drone_list):    
            for j, other_drone in enumerate(drone_list):
                if j > i:
                    # Calculate the distance only for drones in the air
                    distance = np.linalg.norm(np.array(drone['position']) - np.array(other_drone['position']))
                    # Proceed with collision detection or detour logic if needed
                    if COLLISION_RADIUS < distance <= DRONE_DETECTION_DIAMETER:
                        single_drone(drone, other_drone, MAX_VELOCITY, SAFE_RADIUS, ANG_RATE, DRONE_DETECTION_DIAMETER,
                                     connection,'drone',distance)
                    elif distance <= COLLISION_RADIUS :
                        log_to_db(connection, -1, "EMERGENCY", f"Alert! Alert! a collision accord between drone {drone['id']} and drone {other_drone['id']} at {drone['position']}")
                        fault(connection, drone['id'], other_drone['id'])
                        

            # Check against each obstacle's bounds
            for obstacle in obstacles:
                # Check if the drone's position plus the safe radius intersects the obstacle's bounds
                distance_to_obstacle = np.linalg.norm(np.array(drone['position']) - np.array(obstacle['position'])) # Handle the drone's response to the detected obstacle
                drone_pos = drone['position']
                if (drone_pos[0] >= obstacle['x_min'] - SAFE_RADIUS_FROM_OBSTACLES and drone_pos[0] <= obstacle['x_max'] + SAFE_RADIUS_FROM_OBSTACLES )and \
                    (drone_pos[1] >= obstacle['y_min'] - SAFE_RADIUS_FROM_OBSTACLES and drone_pos[1] <= obstacle['y_max'] + SAFE_RADIUS_FROM_OBSTACLES )and \
                    (drone_pos[2] >= obstacle['z_min'] - SAFE_RADIUS_FROM_OBSTACLES  and drone_pos[2] <= obstacle['z_max'] + SAFE_RADIUS_FROM_OBSTACLES ):

                        
                        single_drone(drone, obstacle,
                                # Use the calculated center position
                                MAX_VELOCITY, SAFE_RADIUS, ANG_RATE, DRONE_DETECTION_DIAMETER, connection, "obstacle",
                                distance_to_obstacle)


                elif distance_to_obstacle <= COLLISION_RADIUS * 2:
                        log_to_db(connection, -1, "EMERGENCY",
                                    f"Alert! Alert! a collision accord between drone {drone['id']} and obstacle {obstacle['id']} at {drone['position']}")
                        fault(connection, drone['id'], other_drone['id'])

# def check_drones_for_collisions_thread(connection,obstacles):
#     while True:
#         start_time = time.time()
#         # Fetch all drones with their latest positions
#         drones = fetch_current_positions(connection)
#         check_drones_for_collisions(connection,drones,obstacles)
#         # Record the end time
#         end_time = time.time()

#         # Calculate the elapsed time
#         elapsed_time = end_time - start_time

#         # Log the elapsed time
#         print(f"Cycle completed in {elapsed_time:.4f} seconds")
        

def main():

    # Connection parameters - adjust these with your details
    conn = create_database_connection("localhost", "root", "Aa123456789!", "final_project")
    obstacles = generate_obstacles(conn)
    # Run the collision checking in a separate thread
    # collision_thread = threading.Thread(target=check_drones_for_collisions_thread, args=(conn,obstacles,))
    # collision_thread.start()
    while True:
        start_time = time.time()
        
        # Fetch all drones with their latest positions
        drones = fetch_current_positions(conn)
        check_drones_for_collisions(conn,drones,obstacles)
        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Log the elapsed time
        print(f"Cycle completed in {elapsed_time:.4f} seconds")
        time.sleep(0.01)

if __name__ == '__main__':
    main()
# def update_drone_coordinates_thread(connection):
#     while True:
#         try:
#
#             drones = fetch_current_positions(connection)
#
#             for drone in drones:
#                 drone_id = drone[0]  # Assuming drone ID is the first element of the tuple
#                 current_step_index = drone[1]  # Assuming current step index is the second element of the tuple
#
#                 # Fetch the next step for the drone
#                 next_step_query = """
#                 SELECT step_index, drone_x_coordinate, drone_y_coordinate, drone_z_coordinate
#                 FROM steps
#                 WHERE drone_id = %s AND step_index = %s
#                 """
#                 next_step = execute_read_query2(connection, next_step_query ,(drone_id,current_step_index+1))
#
#                 # Check if the next step exists
#                 if next_step:
#                     next_step_data = next_step[0]  # This should be a tuple containing step data
#                     next_step_index = next_step_data[0]  # Correctly extract the index as an integer
#                     next_x = next_step_data[1]
#                     next_y = next_step_data[2]
#                     next_z = next_step_data[3]
#
#                     # Update drone coordinates and step index
#                     update_drone_query = """
#                     UPDATE drones
#                     SET drone_x_coordinate = %s,
#                         drone_y_coordinate = %s,
#                         drone_z_coordinate = %s,
#                         step_index = %s
#                     WHERE drone_id = %s
#                     """
#                     execute_write_query(connection, update_drone_query, (next_x, next_y, next_z, next_step_index, drone_id))
#
#                     # Log the movement
#                     log_to_db(connection, drone_id, "INFO", f"Drone {drone_id} moved to step {next_step_index}.")
#                 else:
#                     # Handle case where there is no next step
#                     log_to_db(connection, drone_id, "WARNING", f"No next step found for Drone {drone_id}. Current step: {current_step_index}")
#
#         except Exception as e:
#             log_to_db(connection, -1, "ERROR", f"Error in updating drone coordinates: {e}")
#
#         # Sleep to reduce the load
#         time.sleep(1)

# Start the drone coordinates updating thread
# update_coordinates_thread = threading.Thread(target=update_drone_coordinates_thread, args=(conn,))
# update_coordinates_thread.start()

# Keep the main program running
# while True:
#     time.sleep(1)  # This keeps the main thread alive without affecting the other threads