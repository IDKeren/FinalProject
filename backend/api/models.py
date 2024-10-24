from django.db import models
from django.utils import timezone

class Bases(models.Model):
    base_id = models.AutoField(primary_key=True)
    base_x_coordinate = models.FloatField(null=True)
    base_y_coordinate = models.FloatField(null=True)
    is_available = models.BooleanField(null=True)

    def __str__(self):
        return f"Base ({self.base_x_coordinate}, {self.base_y_coordinate})"
    class Meta:
        db_table = 'bases' 

class PickupLocations(models.Model):
    pickup_id = models.AutoField(primary_key=True)
    pickup_x_coordinate = models.FloatField(null=True)
    pickup_y_coordinate = models.FloatField(null=True)

    def __str__(self):
        return f"Pickup Location ({self.pickup_x_coordinate}, {self.pickup_y_coordinate})"
    class Meta:
        db_table = 'pickup_locations' 

class DropLocations(models.Model):
    drop_id = models.AutoField(primary_key=True)
    drop_x_coordinate = models.FloatField(null=True)
    drop_y_coordinate = models.FloatField(null=True)

    def __str__(self):
        return f"Drop Location ({self.drop_x_coordinate}, {self.drop_y_coordinate})"
    class Meta:
        db_table = 'drop_locations' 

class Drones(models.Model):
    drone_id = models.AutoField(primary_key=True)
    battery_percentage = models.IntegerField(null=True)
    is_fault = models.BooleanField(null=True)
    is_detouring = models.BooleanField (null=False)
    velocity = models.IntegerField(null=True)
    drone_x_coordinate = models.FloatField(null=True)
    drone_y_coordinate = models.FloatField(null=True)
    drone_z_coordinate = models.FloatField(null=True)
    real_x = models.FloatField(null=False)
    real_y = models.FloatField(null=False)
    real_z = models.FloatField(null=False)
    is_package_load = models.BooleanField(null=True)
    is_package_unload = models.BooleanField(null=True)
    last_communication = models.FloatField(null=True)
    planned_start_time = models.FloatField(null=True)
    step_index = models.IntegerField(null=True)
    base = models.ForeignKey(Bases, on_delete=models.CASCADE, null=True)
    ready_for_delivery = models.BooleanField(null=True)
    last_moved = models.FloatField(null=True)

    def __str__(self):
        return f"Drone ID {self.drone_id}"
    class Meta:
        db_table = 'drones' 

class Deliveries(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    drone = models.ForeignKey(Drones, on_delete=models.CASCADE, null=True)
    drop = models.ForeignKey(DropLocations, on_delete=models.CASCADE, null=True)
    pickup = models.ForeignKey(PickupLocations, on_delete=models.CASCADE, null=True)
    is_collected = models.BooleanField()
    is_delivered = models.BooleanField()
    requested_date = models.IntegerField(null=True)

    def __str__(self):
        return f"Delivery ID {self.delivery_id}"
    class Meta:
        db_table = 'deliveries' 

class Steps(models.Model):
    id = models.AutoField(primary_key=True)
    step_index = models.IntegerField()
    drone_x_coordinate = models.FloatField(null=True)
    drone_y_coordinate = models.FloatField(null=True)
    drone_z_coordinate = models.FloatField(null=True)
    drone = models.ForeignKey(Drones, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Step {self.step_index} for Drone ID {self.drone.drone_id}"
    class Meta:
        db_table = 'steps' 

class Obstacles(models.Model):
    id = models.AutoField(primary_key=True)
    x_min = models.FloatField(null=True)
    x_max = models.FloatField(null=True)
    y_min = models.FloatField(null=True)
    y_max = models.FloatField(null=True)
    z_min = models.FloatField(null=True)
    z_max = models.FloatField(null=True)
    t_start = models.FloatField(null=True)
    t_end = models.FloatField(null=True)
    value = models.IntegerField(null=True)

    def __str__(self):
        return f"Obstacle ID {self.id}"
    class Meta:
        db_table = 'obstacles' 


class Logs(models.Model):
    id = models.AutoField(primary_key=True)
    drone = models.ForeignKey(Drones, on_delete=models.CASCADE, null=True)
    log_message = models.TextField(null=True)
    log_level = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Log ID {self.id}"
    
    class Meta:
        db_table = 'logs' 
