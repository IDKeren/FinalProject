from math import sqrt
from shared import *

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

def check_drone_proximity(conn):
    start_time = time.time()
    collision_count = 0
    query = """
        SELECT d1.drone_id AS drone1_id, d2.drone_id AS drone2_id,
               d1.real_x AS x1, d1.real_y AS y1, d1.real_z AS z1,
               d2.real_x AS x2, d2.real_y AS y2, d2.real_z AS z2,
               SQRT(POW(d1.real_x - d2.real_x, 2) +
                    POW(d1.real_y - d2.real_y, 2) +
                    POW(d1.real_z - d2.real_z, 2)) AS distance
        FROM drones d1
        CROSS JOIN drones d2
        WHERE d1.drone_id < d2.drone_id
        AND d1.step_index != 0
        AND d2.step_index != 0
        ORDER BY distance, d1.last_communication
        """
    while True:
        results = query_db(conn, query)

        if results:
            for row in results:
                drone1_id, drone2_id, x1, y1, z1, x2, y2, z2, distance = row
                if distance < 2:
                    collision_count += 1
                    print(f"amount of collisions: {collision_count}")
                    end_time = time.time()

                    # Calculate the elapsed time
                    elapsed_time = end_time - start_time
                    print(f"elapsed_time: {elapsed_time}")
                    exit()

conn = create_connection()
check_drone_proximity(conn)