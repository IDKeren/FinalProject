import time
import scipy.stats as stats
import mysql.connector

MIN_HEIGHT_FLIGHT = 30  # units: meters
MAX_HEIGHT_FLIGHT = 200  # units: meters
MAX_X = 400  # units: meters       only example!!!!!
MAX_Y = 400  # units: meters       only example!!!!!
FLIGHT_VELOCITY = 10  # units: meters/second
RRT_MAX_STEP = 20  # units: meters, equal to velocity because it represents max meter per second
SAFE_RADIUS = 10  # units: meters
SAFE_CUBE_RADIUS = 12 #units: meters
OBSTACLE_WEIGHT = 10
SEGMENT_SAMPLING_AMOUNT = 20
LOCATION_INDEX_FOR_X = 0
LOCATION_INDEX_FOR_Y = 1
LOCATION_INDEX_FOR_Z = 2
LOCATION_INDEX_FOR_T = 3
RRT_ITERATIONS = 1250
BASE_AREA = 10   # units: meters
REACH_AREA = 5.5  # units: meters
WANTED_CERTAINTY = 7/12  # this is the certainty we want to have before claiming the drone reach a step,
                        # it can be even higher depending on the distance from target
GPS_FREQUENCY = 10  # units: Hz
GPS_SAMPLE_SPEED = 1/GPS_FREQUENCY  # units: seconds
# I take 3% mean error for wind because (drones withstand, seasons, max speed, time to correct)
MEAN_WIND_ERROR = (FLIGHT_VELOCITY * 3/100) * GPS_SAMPLE_SPEED  # units: meters
MEAN_POSITIONING_ERROR = 2.64#2.64  # units: meters, this is according to the article

TEMP_HEIGHT = 115  # units: meters
LAST_DELIVERY_TIME = 0
DELIVERY_GAPS = 3
WAIT_TIME_FOR_DELIVERY = 7  # units: sec

system_time = time.time()
z_score = stats.norm.ppf((1 + WANTED_CERTAINTY) / 2)
certainty_range = z_score * MEAN_POSITIONING_ERROR
trustable_range = REACH_AREA - certainty_range

miss_loc_count = 0
ministeps_to_step = 0
class Delivery:
    def __init__(self, delivery_id, drone_id, drop_id, pickup_id, is_collected, is_delivered,
                 requested_date):
        self.delivery_id = delivery_id
        self.drone_id = drone_id
        self.drop_id = drop_id
        self.pickup_id = pickup_id
        self.is_collected = is_collected
        self.is_delivered = is_delivered
        self.requested_date = requested_date


class DroneStopLocation:
    def __init__(self, location_id, x, y):
        self.location_id = location_id
        self.x = x
        self.y = y


class Step:
    def __init__(self, id, step_index, x, y, z, drone_id):
        self.id = id
        self.step_index = step_index
        self.x = x
        self.y = y
        self.z = z
        self.drone_id = drone_id


class Base:
    def __init__(self, base_id, x, y, is_available):
        self.base_id = base_id
        self.x = x
        self.y = y
        self.is_available = is_available


class Drone:
    def __init__(self, drone_id, battery_percentage, is_fault, is_detouring, velocity, false_x, false_y, false_z, real_x, real_y,
                 real_z, is_package_load, is_package_unload, last_communication, planned_start_time, step_index,
                 base_id, ready_for_delivery, last_moved):
        self.drone_id = drone_id
        self.battery_percentage = battery_percentage
        self.is_fault = is_fault
        self.velocity = velocity
        self.false_x_coord = false_x
        self.false_y_coord = false_y
        self.false_z_coord = false_z
        self.real_x_coord = real_x
        self.real_y_coord = real_y
        self.real_z_coord = real_z
        self.is_package_load = is_package_load
        self.is_package_unload = is_package_unload
        self.last_communication = last_communication
        self.planned_start_time = planned_start_time
        self.step_index = step_index
        self.base_id = base_id
        self.ready_for_delivery = ready_for_delivery
        self.last_moved = last_moved

def query_db(conn, query):
    cursor = conn.cursor(buffered=False)
    try:
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        conn.commit()
        cursor.close()
    return None