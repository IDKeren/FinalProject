# import numpy as np
# from rrt_star_functions import Node
# import random
#
#
# # this function from rrt_star_functions.py
# def distance_to_segment(self, point, node1, node2):
#     v = node2.coords - node1.coords
#     w = point - node1.coords
#     c1 = np.dot(w, v)
#     if c1 <= 0:
#         return self.distance(Node(point), node1)
#     c2 = np.dot(v, v)
#     if c2 <= c1:
#         return self.distance(Node(point), node2)
#     b = c1 / c2
#     pb = node1.coords + b * v
#     return np.linalg.norm(point - pb)
#
#
# def create_3d_obstacle_map():
#     # init
#     x_dim = 100
#     y_dim = 100
#     z_dim = 200
#     obstacle_value = 10
#     obstacle_percentage = 0.1
#
#     # Create an empty map
#     obstacle_map = np.zeros((x_dim, y_dim, z_dim), dtype=int)
#
#     # Calculate the number of obstacle cells
#     total_cells = x_dim * y_dim * z_dim
#     num_obstacle_cells = int(total_cells * obstacle_percentage)
#
#     # Randomly choose unique indices for obstacle cells
#     obstacle_indices = random.sample(range(total_cells), num_obstacle_cells)
#
#     # Mark the obstacle cells in the map
#     for index in obstacle_indices:
#         x = index // (y_dim * z_dim)
#         y = (index % (y_dim * z_dim)) // z_dim
#         z = index % z_dim
#         obstacle_map[x, y, z] = obstacle_value
#
#     return obstacle_map


# -- Create the database
# CREATE DATABASE final_project;
#
# -- Use the database
# USE final_project;
#
# -- Create the tables
# CREATE TABLE pickup_locations (
#     pickup_id INT AUTO_INCREMENT PRIMARY KEY,
#     pickup_x_coordinate FLOAT,
#     pickup_y_coordinate FLOAT
# );
#
# CREATE TABLE drop_locations (
#     drop_id INT AUTO_INCREMENT PRIMARY KEY,
#     drop_x_coordinate FLOAT,
#     drop_y_coordinate FLOAT
# );
#
# CREATE TABLE bases (
#     base_id INT AUTO_INCREMENT PRIMARY KEY,
#     base_x_coordinate FLOAT,
#     base_y_coordinate FLOAT,
#     is_available TINYINT(1)
# );
#
# CREATE TABLE drones (
#     drone_id INT AUTO_INCREMENT PRIMARY KEY,
#     battery_percentage INT,
#     is_fault TINYINT(1),
#     velocity INT,
#     drone_x_coordinate FLOAT,
#     drone_y_coordinate FLOAT,
#     drone_z_coordinate FLOAT,
#     is_package_load TINYINT(1),
#     is_package_unload TINYINT(1),
#     last_communication INT,
#     planned_start_time INT,
#     step_index INT,
#     base_id INT,
#     ready_for_delivery TINYINT(1),
#     FOREIGN KEY (base_id) REFERENCES bases(base_id)
# );
#
# CREATE TABLE steps (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     step_index INT,
#     drone_x_coordinate FLOAT,
#     drone_y_coordinate FLOAT,
#     drone_z_coordinate FLOAT,
#     drone_id INT,
#     FOREIGN KEY (drone_id) REFERENCES drones(drone_id)
# );
#
# CREATE TABLE deliveries (
#     delivery_id INT AUTO_INCREMENT PRIMARY KEY,
#     drone_id INT,
#     drop_id INT,
#     pickup_id INT,
#     is_collected,
#     is_delivered,
#     delivery_date INT,
#     FOREIGN KEY (drone_id) REFERENCES drones(drone_id),
#     FOREIGN KEY (drop_id) REFERENCES drop_locations(drop_id),
#     FOREIGN KEY (pickup_id) REFERENCES pickup_locations(pickup_id)
# );

# INSERT INTO bases (base_x_coordinate, base_y_coordinate, is_available)
# VALUES
#     ( 3, 26, TRUE),
#     ( 20, 6, TRUE)

# INSERT INTO pickup_locations (pickup_x_coordinate, pickup_y_coordinate)
# VALUES
#     ( 7, 4),
#     ( 12, 19)

# INSERT INTO drop_locations (drop_x_coordinate, drop_y_coordinate)
# VALUES
#     ( 9, 9),
#     ( 22, 12)


# INSERT INTO deliveries (drone_id, drop_id, pickup_id, is_collected, is_delivered, requested_date)
# VALUES
#     (NULL, 1, 1, FALSE, FALSE, 1723216397),
#     (NULL, 1, 2, FALSE, FALSE, 1723216397),
#     (NULL, 2, 1, FALSE, FALSE, 1723216397),
#     (NULL, 2, 2, FALSE, FALSE, 1723216397)

# INSERT INTO drones
#     (battery_percentage, is_fault, velocity, drone_x_coordinate, drone_y_coordinate, drone_z_coordinate,
#      is_package_load, is_package_unload, last_communication, planned_start_time, step_index, base_id, ready_for_delivery)
# VALUES
# (85.5, FALSE, 3, 3, 26, 0, TRUE, FALSE, 1723216397, 0, 0, 1, TRUE),
# (90, FALSE, 3, 3, 26, 0, TRUE, FALSE, 1723216397, 0, 0, 1, TRUE),
# (98, FALSE, 3, 3, 26, 0, TRUE, FALSE, 1723216397, 0, 0, 1, TRUE),
# (95, FALSE, 3, 3, 26, 0, TRUE, FALSE, 1723216397, 0, 0, 1, TRUE),
# (88, FALSE, 3, 20, 6, 0, TRUE, FALSE, 1723216397, 0, 0, 2, TRUE),
# (88, FALSE, 0, 20, 6, 0, FALSE, FALSE, 1723216397, 0, 0, 2, TRUE),
# (88, FALSE, 0, 20, 6, 0, FALSE, FALSE, 1723216397, 0, 0, 2, TRUE),
# (88, FALSE, 0, 20, 6, 0, FALSE, FALSE, 1723216397, 0, 0, 2, TRUE),



#
# import numpy as np
# import random
#
#
# def create_4d_obstacle_map(
#         x_dim: int,
#         y_dim: int,
#         z_dim: int,
#         t_dim: int,
#         obstacle_percentage: float = 0.1,
#         obstacle_weight: int = 10,
#         special_weight: int = 8,
#         num_special_points: int = 6) -> np.ndarray:
#     # Initialize the map with zeros
#     obstacle_map = np.zeros((x_dim, y_dim, z_dim, t_dim), dtype=int)
#
#     # Calculate the number of random obstacles to place
#     total_points = x_dim * y_dim
#     num_obstacles = int(total_points * obstacle_percentage)
#
#     # Place random obstacles with weight=10
#     for _ in range(num_obstacles):
#         x = random.randint(0, x_dim - 1)
#         y = random.randint(0, y_dim - 1)
#         max_z = random.randint(1, z_dim)  # Random max z value between 1 and 40
#         obstacle_map[x, y, :max_z, :] = obstacle_weight
#
#     # Place 6 special points with weight=8 for all z and t
#     special_points = []
#     for _ in range(num_special_points):
#         while True:
#             x = random.randint(0, x_dim - 1)
#             y = random.randint(0, y_dim - 1)
#
#             # Ensure the point is not already an obstacle
#             if np.all(obstacle_map[x, y, :, :] == 0):
#                 obstacle_map[x, y, :, :] = special_weight
#                 special_points.append((x, y))
#                 break
#
#     return obstacle_map, special_points
#
#
# # Set dimensions for the map
# x_dim, y_dim, z_dim, t_dim = 40, 40, 40, 1200
#
# # Create the obstacle map
# obstacle_map, special_points = create_4d_obstacle_map(x_dim, y_dim, z_dim, t_dim)
#
# # Save the obstacle map to a file
# output_file_path = '4d_obstacle_map.npy'
# np.save(output_file_path, obstacle_map)
#
# # Print the coordinates of the special points
# print(f"4D obstacle map saved to {output_file_path}")
# print("Special points added (x, y):")
# for point in special_points:
#     print(point)



#------------------create 10% obstacles--------------------------------
# import mysql.connector
# import random
#
# # Database connection configuration
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'database': 'final_project'
# }
#
# # Connect to the database
# try:
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     print("Connected to database successfully")
# except mysql.connector.Error as err:
#     print(f"Error connecting to database: {err}")
#     exit(1)
#
# # Create the obstacles table if it doesn't exist
# create_table_query = """
# CREATE TABLE IF NOT EXISTS obstacles (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     x_min DECIMAL(6,1),
#     x_max DECIMAL(6,1),
#     y_min DECIMAL(6,1),
#     y_max DECIMAL(6,1),
#     z_min DECIMAL(6,1),
#     z_max DECIMAL(6,1),
#     t_start DECIMAL(12,1),
#     t_end DECIMAL(12,1),
#     value INT
# )
# """
# cursor.execute(create_table_query)
# print("Table 'obstacles' created or already exists")
#
# # Clear existing data
# cursor.execute("TRUNCATE TABLE obstacles")
# print("Existing data cleared from 'obstacles' table")
#
#
# def format_float(value):
#     return f"{value:.1f}"
#
#
# def check_overlap(new_obstacle, existing_obstacles):
#     for obs in existing_obstacles:
#         if (new_obstacle[0] < obs[1] and new_obstacle[1] > obs[0] and
#                 new_obstacle[2] < obs[3] and new_obstacle[3] > obs[2]):
#             return True
#     return False
#
#
# # Generate and insert obstacles
# map_size = 400
# coverage_percentage = 0.06  # 6% coverage
# total_area = map_size * map_size
# target_obstacle_area = total_area * coverage_percentage
# existing_obstacles = []
# current_obstacle_area = 0
#
# insert_query = """
# INSERT INTO obstacles (x_min, x_max, y_min, y_max, z_min, z_max, t_start, t_end, value)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
# """
#
# try:
#     max_attempts = 10000  # Limit attempts to prevent infinite loop
#     attempts = 0
#
#     while current_obstacle_area < target_obstacle_area and attempts < max_attempts:
#         # Generate obstacle dimensions
#         width = round(random.uniform(3, 20), 1)
#         height = round(random.uniform(3, 20), 1)
#
#         # Generate obstacle position
#         x = round(random.uniform(0, map_size - width), 1)
#         y = round(random.uniform(0, map_size - height), 1)
#
#         new_obstacle = (x, x + width, y, y + height)
#
#         if not check_overlap(new_obstacle, existing_obstacles):
#             # Generate z values
#             z_max = round(random.uniform(30, 200), 1)
#
#             values = (
#                 format_float(x), format_float(x + width),
#                 format_float(y), format_float(y + height),
#                 format_float(0), format_float(z_max),
#                 format_float(0), '10000000000.0',  # 1e+10 as a string
#                 10
#             )
#
#             cursor.execute(insert_query, values)
#             existing_obstacles.append(new_obstacle)
#             current_obstacle_area += width * height
#
#         attempts += 1
#
#     conn.commit()
#     print(f"Successfully inserted obstacles covering {current_obstacle_area:.2f} square units")
#     print(f"Target area was {target_obstacle_area:.2f} square units")
#     print(f"Actual coverage: {(current_obstacle_area / total_area) * 100:.2f}%")
#     if attempts >= max_attempts:
#         print("Warning: Reached maximum attempts. The map might not be fully populated.")
#
# except mysql.connector.Error as err:
#     conn.rollback()
#     print(f"Error inserting data: {err}")



#--------------------------create 15 bases -------------------------------------
# import mysql.connector
# import random
#
# # Database connection configuration
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'database': 'final_project'
# }
#
# # Connect to the database
# try:
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()
#     print("Connected to database successfully")
# except mysql.connector.Error as err:
#     print(f"Error connecting to database: {err}")
#     exit(1)
#
#
# def format_float(value):
#     return f"{value:.1f}"
#
#
# # Function to check if a new obstacle overlaps with existing obstacles
# def check_overlap(new_obstacle, obstacles):
#     for obs in obstacles:
#         if (new_obstacle[0] < obs[1] and new_obstacle[1] > obs[0] and
#                 new_obstacle[2] < obs[3] and new_obstacle[3] > obs[2]):
#             return True
#     return False
#
#
# # Fetch all existing obstacles
# cursor.execute("SELECT x_min, x_max, y_min, y_max FROM obstacles")
# existing_obstacles = cursor.fetchall()
#
# # Generate and insert 15 new 20x20 obstacles
# new_obstacles = []
# insert_query = """
# INSERT INTO obstacles (x_min, x_max, y_min, y_max, z_min, z_max, t_start, t_end, value)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
# """
#
# try:
#     max_attempts = 1000  # Maximum number of attempts to find non-overlapping positions
#     attempt_count = 0
#
#     while len(new_obstacles) < 15 and attempt_count < max_attempts:
#         x = round(random.uniform(0, 390), 1)  # 190 to ensure the 10x10 obstacle fits within the 200x200 map
#         y = round(random.uniform(0, 390), 1)
#
#         new_obstacle = (x, x + 20, y, y + 20)
#
#         if not check_overlap(new_obstacle, existing_obstacles + new_obstacles):
#             values = (
#                 format_float(x), format_float(x + 20),
#                 format_float(y), format_float(y + 20),
#                 format_float(0), format_float(200),
#                 format_float(0), '10000000000.0',  # 1e+10 as a string
#                 8
#             )
#
#             cursor.execute(insert_query, values)
#             new_obstacles.append(new_obstacle)
#         else:
#             attempt_count += 1
#
#     conn.commit()
#     print(f"Successfully inserted {len(new_obstacles)} new 10x10 obstacles")
#     if attempt_count >= max_attempts:
#         print(f"Warning: Reached maximum attempts. Only {len(new_obstacles)} obstacles were placed.")
#
# except mysql.connector.Error as err:
#     conn.rollback()
#     print(f"Error inserting data: {err}")
#
# # Print the new obstacles and their center coordinates
# print("\nInserted 10x10 Obstacles:")
# print("ID\tX_min\tX_max\tY_min\tY_max\tCenter X\tCenter Y")
# for i, (x_min, x_max, y_min, y_max) in enumerate(new_obstacles, 1):
#     center_x = (x_min + x_max) / 2
#     center_y = (y_min + y_max) / 2
#     print(f"{i}\t{x_min}\t{x_max}\t{y_min}\t{y_max}\t{center_x:.1f}\t{center_y:.1f}")
#
# # Verify the total insertion
# cursor.execute("SELECT COUNT(*) FROM obstacles")
# total_obstacles = cursor.fetchone()[0]
# print(f"\nTotal objects in the table: {total_obstacles}")
#
# # Close the database connection
# cursor.close()
# conn.close()


import mysql.connector
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np



def visualize_weight_map(time, points=None, nodes = None):
    """
    Visualize obstacles in 3D at a specific time and plot additional points.

    :param points: List of [x,y,z] coordinates to plot as black 'x' markers
    :param time: The time at which to visualize obstacles (default is 1)
    """
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'database': 'final_project'
    }
    # Connect to the database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return

    # Fetch obstacle data
    query = f"""
    SELECT x_min, x_max, y_min, y_max, z_min, z_max, value
    FROM obstacles
    WHERE t_start <= {time} AND t_end >= {time}
    """
    cursor.execute(query)
    obstacles = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Prepare the 3D plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Color map for different values
    color_map = {8: 'red', 10: 'blue'}  # Add more colors if you have more distinct values

    # Plot each obstacle
    for obs in obstacles:
        x_min, x_max, y_min, y_max, z_min, z_max, value = obs

        # Create the vertices of the cuboid
        xx, yy = np.meshgrid([x_min, x_max], [y_min, y_max])

        # Plot the bottom face
        ax.plot_surface(xx, yy, np.full_like(xx, z_min), color=color_map.get(value, 'gray'), alpha=0.5)

        # Plot the top face
        ax.plot_surface(xx, yy, np.full_like(xx, z_max), color=color_map.get(value, 'gray'), alpha=0.5)

        # Plot the vertical edges
        for x, y in zip(xx.flat, yy.flat):
            ax.plot([x, x], [y, y], [z_min, z_max], color=color_map.get(value, 'gray'), alpha=0.5)

    if nodes is not None:
        # Extract coordinates from Node instances
        points = np.array([node.coords for node in nodes])
    # Plot additional points if provided
    if points is not None:
        points = np.array(points)
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='black', marker='x', s=50, label='Additional Points')

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'3D Visualization of Obstacles at t={time}')

    # Set axis limits
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 400)
    ax.set_zlim(0, 200)

    # Add a color legend
    legend_elements = [plt.Rectangle((0, 0), 1, 1, fc=color, alpha=0.5, label=f'Value {val}')
                       for val, color in color_map.items()]
    legend_elements.append(plt.Line2D([0], [0], marker='x', color='w', markerfacecolor='black', markersize=10, label='Additional Points'))
    ax.legend(handles=legend_elements, loc='upper right')

    # Show the plot
    plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
# # Example data
# # Replace this with your actual 4D ndarray
# data = np.random.rand(40, 40, 40, 1200)  # Replace with your actual data
#
#
# def visualize_map_at_time(t_index, data, additional_nodes=None, additional_coords=None, block = False):
#     if t_index < 0 or t_index >= data.shape[3]:
#         print(f"Time index {t_index} is out of bounds.")
#         return
#
#     # Extract the 3D slice for the given t_index
#     slice_3d = data[:, :, :, t_index]
#
#     # Get the coordinates and weights of non-zero points
#     x, y, z = np.nonzero(slice_3d)
#     weights = slice_3d[x, y, z]
#
#     # Create a 3D scatter plot
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#
#     # Plot the main scatter plot with weights
#     scatter = ax.scatter(x, y, z, c=weights, cmap='viridis', marker='o')
#
#     # Plot additional points in black if provided
#     if additional_nodes is not None:
#         # Extract coordinates from Node instances
#         additional_coords = np.array([node.coords for node in additional_nodes])
#     if additional_coords is not None:
#         additional_coords = np.array(additional_coords)
#     # Extract coordinates and time steps from the additional points
#     if additional_coords is not None:
#         if additional_coords.shape[1] != 4:
#             print("Additional points should be in the form (x, y, z, t).")
#             return
#
#         # Filter points for the specific time step
#         x_add, y_add, z_add, t_add = additional_coords.T
#
#         # Plot additional points in black
#         ax.scatter(x_add, y_add, z_add, c='k', marker='x', label='Additional Points')
#
#     # Add a color bar
#     cbar = plt.colorbar(scatter, ax=ax)
#     cbar.set_label('Weight')
#
#     # Set labels and title
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
#     ax.set_zlabel('Z')
#     ax.set_title(f'3D Scatter Plot for t = {t_index}')
#
#     # Add legend if additional points are plotted
#     if additional_coords is not None:
#         ax.legend()
#
#     plt.show(block=block)


