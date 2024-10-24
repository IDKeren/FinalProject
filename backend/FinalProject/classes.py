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


class DroneMidLocation:
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
    def __init__(self, drone_id, battery_percentage, is_fault, velocity, x, y, z, is_package_load, is_package_unload,
                 last_communication, planned_start_time, step_index, base_id, ready_for_delivery):
        self.drone_id = drone_id
        self.battery_percentage = battery_percentage
        self.is_fault = is_fault
        self.velocity = velocity
        self.x_coord = x
        self.y_coord = y
        self.z_coord = z
        self.is_package_load = is_package_load
        self.is_package_unload = is_package_unload
        self.last_communication = last_communication
        self.planned_start_time = planned_start_time
        self.step_index = step_index
        self.base_id = base_id
        self.ready_for_delivery = ready_for_delivery
