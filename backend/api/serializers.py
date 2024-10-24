from rest_framework import serializers
from .models import PickupLocations, DropLocations, Bases, Drones, Steps, Deliveries,Obstacles,Logs


class PickupLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupLocations
        fields = ['pickup_id', 'pickup_x_coordinate', 'pickup_y_coordinate']

class ObstaclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obstacles
        fields = [
            'id',
            'x_min',
            'x_max',
            'y_min',
            'y_max',
            'z_min',
            'z_max',
            't_start',
            't_end',
            'value',
        ]


class DropLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropLocations
        fields = ['drop_id', 'drop_x_coordinate', 'drop_y_coordinate']


class BasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bases
        fields = ['base_id', 'base_x_coordinate', 'base_y_coordinate', 'is_available']


class DronesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drones
        fields = [  
            'drone_id', 'battery_percentage', 'is_fault', 'is_detouring','velocity',
            'drone_x_coordinate', 'drone_y_coordinate', 'drone_z_coordinate',
            'real_x', 'real_y', 'real_z',
            'is_package_load', 'is_package_unload', 'last_communication',
            'planned_start_time', 'step_index', 'base', 'ready_for_delivery', 'last_moved'
        ]


class StepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Steps
        fields = ['step_index', 'drone_x_coordinate', 'drone_y_coordinate', 'drone_z_coordinate', 'drone']


class DeliveriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliveries
        fields = [
            'delivery_id', 'drone', 'drop', 'pickup',
            'is_collected', 'is_delivered', 'requested_date'  # Changed from delivery_date
        ]




class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = [
            'id', 'drone_id', 'log_message', 'log_level',
            'timestamp'
        ]

