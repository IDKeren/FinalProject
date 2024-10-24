-- Drop the database if it exists
DROP DATABASE IF EXISTS final_project;

-- Create the database
CREATE DATABASE final_project;

-- Use the database
USE final_project;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS deliveries;
DROP TABLE IF EXISTS steps;
DROP TABLE IF EXISTS drones;
DROP TABLE IF EXISTS bases;
DROP TABLE IF EXISTS drop_locations;
DROP TABLE IF EXISTS pickup_locations;
DROP TABLE IF EXISTS obstacles;

-- Create the tables
CREATE TABLE pickup_locations (
    pickup_id INT AUTO_INCREMENT PRIMARY KEY,
    pickup_x_coordinate FLOAT,
    pickup_y_coordinate FLOAT
);

CREATE TABLE drop_locations (
    drop_id INT AUTO_INCREMENT PRIMARY KEY,
    drop_x_coordinate FLOAT,
    drop_y_coordinate FLOAT
);

CREATE TABLE bases (
    base_id INT AUTO_INCREMENT PRIMARY KEY,
    base_x_coordinate FLOAT,
    base_y_coordinate FLOAT,
    is_available TINYINT(1)
);

CREATE TABLE drones (
    drone_id INT AUTO_INCREMENT PRIMARY KEY,
    battery_percentage INT,
    is_fault TINYINT(1),
    velocity INT,
    drone_x_coordinate FLOAT,
    drone_y_coordinate FLOAT,
    drone_z_coordinate FLOAT,
    is_package_load TINYINT(1),
    is_package_unload TINYINT(1),
    last_communication INT,
    planned_start_time INT,
    step_index INT,
    base_id INT,
    ready_for_delivery TINYINT(1),
    FOREIGN KEY (base_id) REFERENCES bases(base_id)
);

CREATE TABLE steps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    step_index INT,
    drone_x_coordinate FLOAT,
    drone_y_coordinate FLOAT,
    drone_z_coordinate FLOAT,
    drone_id INT,
    FOREIGN KEY (drone_id) REFERENCES drones(drone_id)
);

CREATE TABLE deliveries (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    drone_id INT,
    drop_id INT,
    pickup_id INT,
    is_collected TINYINT(1),  -- Data type added for 'is_collected'
    is_delivered TINYINT(1),  -- Data type added for 'is_delivered'
    requested_date INT,
    FOREIGN KEY (drone_id) REFERENCES drones(drone_id),
    FOREIGN KEY (drop_id) REFERENCES drop_locations(drop_id),
    FOREIGN KEY (pickup_id) REFERENCES pickup_locations(pickup_id)
);

-- Insert values into 'bases' table
INSERT INTO bases (base_x_coordinate, base_y_coordinate, is_available)
VALUES
    (3, 26, 1),  -- Use 1 instead of TRUE for boolean
    (20, 6, 1);  -- Use 1 instead of TRUE for boolean

-- Insert values into 'pickup_locations' table
INSERT INTO pickup_locations (pickup_x_coordinate, pickup_y_coordinate)
VALUES
    (7, 4),
    (12, 19);

-- Insert values into 'drop_locations' table
INSERT INTO drop_locations (drop_x_coordinate, drop_y_coordinate)
VALUES
    (9, 9),
    (22, 12);

-- Insert values into 'deliveries' table
INSERT INTO deliveries (drone_id, drop_id, pickup_id, is_collected, is_delivered, requested_date)
VALUES
    (NULL, 1, 1, 0, 0, 1723216397),  -- Use 0 instead of FALSE
    (NULL, 1, 2, 0, 0, 1723216397),
    (NULL, 2, 1, 0, 0, 1723216397),
    (NULL, 2, 2, 0, 0, 1723216397);

-- Insert values into 'drones' table
INSERT INTO drones
    (battery_percentage, is_fault, velocity, drone_x_coordinate, drone_y_coordinate, drone_z_coordinate,
     is_package_load, is_package_unload, last_communication, planned_start_time, step_index, base_id, ready_for_delivery)
VALUES
(85, 0, 0, 3, 26, 0, 0, 0, 1723216397, 0, 0, 1, 1),  -- Use 0 instead of FALSE, 1 instead of TRUE
(90, 0, 0, 3, 26, 0, 0, 0, 1723216397, 0, 0, 1, 1),
(98, 0, 0, 3, 26, 0, 0, 0, 1723216397, 0, 0, 1, 1),
(95, 0, 0, 3, 26, 0, 0, 0, 1723216397, 0, 0, 1, 1),
(88, 0, 0, 20, 6, 0, 0, 0, 1723216397, 0, 0, 2, 1),
(88, 0, 0, 20, 6, 0, 0, 0, 1723216397, 0, 0, 2, 1),
(88, 0, 0, 20, 6, 0, 0, 0, 1723216397, 0, 0, 2, 1),
(88, 0, 0, 20, 6, 0, 0, 0, 1723216397, 0, 0, 2, 1);
