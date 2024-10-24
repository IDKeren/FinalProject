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
matplotlib.use('TkAgg')

# Constants for the detour algorithm
MAX_VELOCITY = 10  # Maximum velocity (example value)
SAFE_RADIUS = 15  # Safe radius for each drone
COLLISION_RADIUS = 2.63 # High collision potential radius
ANG_RATE = 150  # Angular rate in degrees per second for commercial drones acroding to the article
DRONE_DETECTION_DIAMETER = 25  # Detection radius of each drone

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

def execute_read_query(connection, query, retries=3):
    for attempt in range(retries):
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            log_to_db(connection, -1, "System: WARNING", f"Read query error: '{e}' - attempt {attempt + 1}")
            if attempt == retries - 1:
                log_to_db(connection, -1, "System: ERROR", "Max retries reached. Skipping this query.")
                return []
        except Exception as ex:
            log_to_db(connection, -1, "System: ERROR", f"Unexpected error: {ex}")
            return []

def execute_write_query(connection, query, data):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()

    except Error as e:
        print(f"The error '{e}' occurred")

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
    detouring = drone.get('is_detouring')  # Fetch detouring status from the drone dictionary

    if(detouring == 0):
        # for obstacle in obstacles:
        #     # Calculate the 3D distance between drones
        #     query = f"SELECT check_distance_alert({drone['position'][0]}, {drone['position'][1]}, {drone['position'][2]}, {obstacle['position'][0]}, {obstacle['position'][1]}, {obstacle['position'][2]}, {detectionR})"
        #     alert_message = execute_read_query(connection, query)
        #
        #     # Check if the query returned any result
        #     if alert_message and len(alert_message) > 0 and 'Alert' in alert_message[0][0]:
                log_to_db(connection, drone['id'], "WARNING", f"Alert: Drone {drone['id']} with cordinates {drone['position']} is too close! to drone {obstacle['id']} Distance: {distance} ,meters")  # Log the alert message

                # Continue with detour logic if an alert is raised
                vlos = np.array(obstacle['position']) - np.array(drone['position'])
                Vod = np.array(obstacle['velocity']) - np.array(drone['velocity'])
                angle_gamma = angle_between(Vod, vlos)

                # Check if the drone is within the safe radius of the obstacle
                distance_to_obstacle = np.linalg.norm(vlos)
                if distance_to_obstacle < safeR or (
                        -90 <= angle_gamma <= 90 and distance_to_obstacle * np.sin(np.radians(angle_gamma)) < safeR):
                    if not detouring:
                        # Update drone status to detouring and reduce speed
                        velocity = maxV / 2
                        detour_steps = calculate_dynamic_detour_steps(drone, obstacle, vlos, Vod, angle_gamma, safeR)
                        insert_detour_steps(connection, drone['id'], detour_steps)

                        #detouring = True
                        #drone['detouring'] = True
                        # Update detouring status
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
    if angle_gamma > 0:
        detour_direction = np.cross(detour_direction, vlos_norm)  # Adjust direction based on relative velocity
        detour_direction = detour_direction / np.linalg.norm(detour_direction)

    # Scale detour direction by the safe radius to move the drone away
    detour_distance = safeR
    step1 = np.array(drone['position']) + detour_direction * detour_distance
    step2 = step1 + detour_direction * detour_distance
    step3 = step2 + detour_direction * detour_distance

    # Define detour steps as tuples with step index and coordinates
    detour_steps = [
        (1, step1[0], step1[1], step1[2], drone['id']),
        (2, step2[0], step2[1], step2[2], drone['id']),
        (3, step3[0], step3[1], step3[2], drone['id'])
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
    step1 = drone_pos + direction * safeR
    step2 = step1 + direction * safeR
    step3 = step2 + direction * safeR

    detour_steps = [
        (1, step1[0], step1[1], step1[2], drone['id']),
        (2, step2[0], step2[1], step2[2], drone['id']),
        (3, step3[0], step3[1], step3[2], drone['id'])
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

def insert_detour_steps(connection, drone_id, detour_steps):
    """
    Insert detour steps into the steps table starting from the current step index,
    and update subsequent steps' indexes accordingly.
    """
    try:
        # Step 1: Fetch the current step index of the drone
        current_step_query = """
        SELECT step_index
        FROM steps
        WHERE drone_id = %s
        ORDER BY step_index
        LIMIT 1
        """
        current_step = execute_read_query(connection, current_step_query % drone_id)

        expected_detouring_step = current_step[0][0] + 3
        update_drone_detour_status(connection, drone_id, expected_detouring_step)

        if current_step:
            # Use the current step index as the starting point for the new detour steps
            current_step_index = current_step[0][0]
            next_index = current_step_index + 1
            # Step 2: Update subsequent steps to make space for new detour steps
            step_increase = len(detour_steps)  # Number of detour steps being inserted
            update_steps_query = """
            UPDATE steps
            SET step_index = step_index + %s
            WHERE drone_id = %s AND step_index >= %s
            """
            execute_write_query(connection, update_steps_query, (step_increase, drone_id, next_index))

            # Step 3: Insert detour steps starting from the current step index
            insert_query = """
            INSERT INTO steps (step_index, drone_x_coordinate, drone_y_coordinate, drone_z_coordinate, drone_id)
            VALUES (%s , %s, %s, %s, %s)
            """

            # Adjust the step indices of the detour steps to start from the current index
            adjusted_detour_steps = [
                (current_step_index + i+1, step[1], step[2], step[3], drone_id)  # Update step_index and keep other values
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

                execute_write_query(connection, update_drone_query, (current_step_index, drone_id))

            log_to_db(connection, drone_id, "INFO", f"Inserted detour steps for Drone {drone_id} starting from index {current_step_index}.")
            print(f"Inserted detour steps for Drone {drone_id} starting from index {current_step_index}.")

        else:
            log_to_db(connection, drone_id, "WARNING", f"No current step found for Drone {drone_id}. Unable to insert detour steps.")
            print(f"No current step found for Drone {drone_id}. Unable to insert detour steps.")

    except Exception as e:
        log_to_db(connection, drone_id, "ERROR", f"Error inserting detour steps for Drone {drone_id}: {e}")
        print(f"Error inserting detour steps for Drone {drone_id}: {e}")


def terminate_detour(drone, initialVel, connection):
    """
    Terminate the detour when the drone's detouring step index matches the step_index.
    """
    # Perform the query to check if is_detouring matches the current step_index
    check_detour_query = """
    SELECT is_detouring, step_index
    FROM drones
    WHERE drone_id = %s AND is_detouring = step_index
    """

    detour_status = execute_read_query(connection, check_detour_query % drone['id'])

    # Check if the query returned any results, indicating detouring should terminate
    if len(detour_status) > 0:
        # Reset detouring status and detouring step index
        update_drone_detour_status(connection, drone['id'], 0)
        drone['is_detouring'] = 0
        drone['velocity'] = initialVel
        log_to_db(connection, drone['id'], "INFO", f"Drone {drone['id']} has terminated the detour.")

# def terminate_detour(drone, obstacle, initialVel, connection):
#     """
#     Terminate the detour.
#     """
#     if drone.get('is_detouring'):
#         # Fetch the detouring step index for the drone
#         detour_step_index_query = """
#             SELECT is_detouring,step_index
#             FROM drones
#             WHERE drone_id = %s
#             """
#         detour_step_index = execute_read_query(connection, detour_step_index_query % drone['id'])
#
#         if current_step:
#             last_step = current_step[0]
#             distance_to_last_step = np.linalg.norm(
#                 np.array(drone['position']) - np.array([last_step[1], last_step[2], last_step[3]]))
#             if distance_to_last_step < 1.0:  # Assume 1.0 as a threshold for reaching the step
#                 drone['detouring'] = False
#                 drone['velocity'] = initialVel
#                 log_to_db(connection, drone['id'], "INFO", f"Drone {drone['id']} has terminated the detour.")

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
        SELECT drone_id, drone_x_coordinate, drone_y_coordinate, drone_z_coordinate, velocity, is_detouring 
        FROM drones;
        """
    return execute_read_query(connection, query)

def fetch_active_obstacles(connection):
    """
    Fetch active obstacles from the database within the current time frame.
    """
    query = f"""
    SELECT id, x_min, x_max, y_min, y_max, z_min, z_max
    FROM obstacles
    """
    return execute_read_query(connection, query)


def ground_and_remove_steps(connection, drone_id1, drone_id2):
    """
    Sets the z-coordinate of the current step of two drones to zero and removes all other steps.

    :param connection: Database connection object.
    :param drone_id1: ID of the first drone.
    :param drone_id2: ID of the second drone.
    """
    try:
        # Step 1: Fetch the current step index for each drone
        current_step_query = """
        SELECT step_index
        FROM steps
        WHERE drone_id = %s
        ORDER BY step_index
        LIMIT 1
        """

        # Fetch current step for both drones
        current_step1 = execute_read_query(connection, current_step_query % drone_id1)
        current_step2 = execute_read_query(connection, current_step_query % drone_id2)

        # Ensure we have a valid step for both drones
        if not current_step1 or not current_step2:
            log_to_db(connection, -1, "ERROR",
                      f"Unable to fetch current steps for drones {drone_id1} and/or {drone_id2}.")
            return

        current_step_index1 = current_step1[0][0]
        current_step_index2 = current_step2[0][0]

        # Step 2: Set the z-coordinate of the current step to zero for both drones
        update_z_query = """
        UPDATE steps
        SET drone_z_coordinate = 0
        WHERE drone_id = %s AND step_index = %s
        """

        # Update z-coordinate for current steps
        execute_write_query(connection, update_z_query, (drone_id1, current_step_index1))
        execute_write_query(connection, update_z_query, (drone_id2, current_step_index2))

        # Step 3: Remove all other steps for both drones
        delete_other_steps_query = """
        DELETE FROM steps
        WHERE drone_id = %s AND step_index != %s
        """

        # Delete other steps for both drones
        execute_write_query(connection, delete_other_steps_query, (drone_id1, current_step_index1))
        execute_write_query(connection, delete_other_steps_query, (drone_id2, current_step_index2))

        update_drone_query = """
                            UPDATE drones
                            SET step_index = %s
                            WHERE drone_id = %s
                            """
        # Update to the new step index (e.g., first detour step index)

        execute_write_query(connection, update_drone_query, (current_step_index1, drone_id1))
        execute_write_query(connection, update_drone_query, (current_step_index2, drone_id2))

        # Log the action
        log_to_db(connection, drone_id1, "INFO",
                  f"Drone {drone_id1} is falling at step {current_step_index1} and other steps removed.")
        log_to_db(connection, drone_id2, "INFO",
                  f"Drone {drone_id2} is falling at step {current_step_index2} and other steps removed.")

    except Exception as e:
        log_to_db(connection, -1, "ERROR", f"Error grounding drones {drone_id1} and {drone_id2}: {e}")
        print(f"Error grounding drones {drone_id1} and {drone_id2}: {e}")


def draw_drone_locations(drone_list):
    global fig, ax

    # Initialize the plot on the first call
    if fig is None or ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.ion()  # Turn on interactive mode
        plt.show()

    # Clear the previous plot
    ax.clear()

    # Plot the drone positions
    for drone in drone_list:
        ax.scatter(drone['position'][0], drone['position'][1], drone['position'][2], label=f"Drone {drone['id']}")

    # Set labels
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')

    # Update legend only if there are labels
    handles, labels = ax.get_legend_handles_labels()
    if labels:
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)

    # Redraw the plot
    plt.draw()
    plt.pause(0.1)  # Pause briefly to allow the plot to update

def check_drones_for_collisions(connection):
    if connection is None:
        log_to_db(connection, -1, "System: ERROR", "No connection to the database.")
        return
    # Fetch all drones with their latest positions
    drones = fetch_current_positions(connection)
    #drones = fetch_latest_positions(connection)
    obstacles = fetch_active_obstacles(connection)
    # Convert to a list of dictionaries for easier handling
    drone_list = []
    for drone in drones:
        drone_list.append({
            'id': drone[0],
            'position': [drone[1], drone[2], drone[3]],
            'velocity': [drone[4], drone[4], drone[4]],  # Simplified for example; adjust as needed
            'is_detouring': drone[5]
        })

    obstacles_list = []
    for obstacle in obstacles:

        obstacle_position = [
            (obstacle[1] + obstacle[2]) / 2,  # X position (center of x_min and x_max)
            (obstacle[3] + obstacle[4]) / 2,  # Y position (center of y_min and y_max)
            (obstacle[5] + obstacle[6]) / 2  # Z position (center of z_min and z_max)
        ]

        obstacles_list.append({
            'id': f"obstacle_{obstacle[0]}",
            'position': obstacle_position,  # Center position in 3D space
            'x_min': obstacle[1],
            'x_max': obstacle[2],
            'y_min': obstacle[3],
            'y_max': obstacle[4],
            'z_min': obstacle[5],
            'z_max': obstacle[6],
        })

        # Check each drone against only nearby drones and exclude ground drones
        for i, drone in enumerate(drone_list):
            # Skip drones on the ground (z = 0)
            if drone['position'][2] <= 0  :
                continue

            for j, other_drone in enumerate(drone_list):
                if i != j:
                    # Skip other drones on the ground (z = 0)
                    if other_drone['position'][2] <= 0:
                        continue

                    # Calculate the distance only for drones in the air
                    distance = np.linalg.norm(np.array(drone['position']) - np.array(other_drone['position']))

                    # Proceed with collision detection or detour logic if needed
                    if COLLISION_RADIUS * 2 <= distance <= DRONE_DETECTION_DIAMETER:
                        single_drone(drone, other_drone, MAX_VELOCITY, SAFE_RADIUS, ANG_RATE, DRONE_DETECTION_DIAMETER,
                                     connection,'drone',distance)
                    if distance <= COLLISION_RADIUS * 2 :
                        log_to_db(connection, -1, "EMERGENCY", f"Alert! Alert! a collision accord between drone {drone['id']} and drone {other_drone['id']} at {drone['position']}")

                        #ground_and_remove_steps(connection, drone['id'], other_drone['id'])

            # Check against each obstacle's bounds
            for obstacle in obstacles_list:
                # Check if the drone's position plus the safe radius intersects the obstacle's bounds
                drone_pos = drone['position']
                if (obstacle['x_min'] <= drone_pos[0] + SAFE_RADIUS <= obstacle['x_max'] or
                    obstacle['x_min'] <= drone_pos[0] - SAFE_RADIUS <= obstacle['x_max']) and \
                    (obstacle['y_min'] <= drone_pos[1] + SAFE_RADIUS <= obstacle['y_max'] or
                        obstacle['y_min'] <= drone_pos[1] - SAFE_RADIUS <= obstacle['y_max']) and \
                        (obstacle['z_min'] <= drone_pos[2] + SAFE_RADIUS <= obstacle['z_max'] or
                         obstacle['z_min'] <= drone_pos[2] - SAFE_RADIUS <= obstacle['z_max']):

                    distance_to_obstacle = np.linalg.norm(np.array(drone['position']) - np.array(obstacle_position['position']))

                    if distance_to_obstacle <= COLLISION_RADIUS * 2:
                        log_to_db(connection, -1, "EMERGENCY",
                                  f"Alert! Alert! a collision accord between drone {drone['id']} and obstacle {obstacle['id']} at {drone['position']}")
                    # Handle the drone's response to the detected obstacle
                    single_drone(
                        drone,
                        [{'id': obstacle['id'], 'position': obstacle['position']}],
                        # Use the calculated center position
                        MAX_VELOCITY, SAFE_RADIUS, ANG_RATE, DRONE_DETECTION_RADIUS, connection,'obstacle',distance_to_obstacle)

    # Draw the locations of the drones live
    #draw_drone_locations(drone_list)

def check_drones_for_collisions_thread(connection):
    while True:
        start_time = time.time()
        check_drones_for_collisions(connection)
        # Record the end time
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Log the elapsed time
        print(f"Cycle completed in {elapsed_time:.4f} seconds")

        time.sleep(0.1)

# Connection parameters - adjust these with your details
conn = create_database_connection("localhost", "root", "8483403", "DroneDB")

# Run the collision checking in a separate thread
collision_thread = threading.Thread(target=check_drones_for_collisions_thread, args=(conn,))
collision_thread.daemon = True  # Make thread a daemon so it terminates with the main program
collision_thread.start()

# Keep the plotting in the main thread
while True:
    time.sleep(1)  # Keep the main thread alive