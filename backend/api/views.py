from django.shortcuts import render
from rest_framework import viewsets
from .models import PickupLocations, DropLocations, Bases, Drones, Steps, Deliveries,Obstacles,Logs
from .serializers import PickupLocationsSerializer, LogsSerializer,DropLocationsSerializer, ObstaclesSerializer,BasesSerializer, DronesSerializer, StepsSerializer, DeliveriesSerializer


class PickupLocationsViewSet(viewsets.ModelViewSet):
    queryset = PickupLocations.objects.all()
    serializer_class = PickupLocationsSerializer

class ObstaclesViewSet(viewsets.ModelViewSet):
    queryset = Obstacles.objects.all()
    serializer_class = ObstaclesSerializer

class DropLocationsViewSet(viewsets.ModelViewSet):
    queryset = DropLocations.objects.all()
    serializer_class = DropLocationsSerializer

class BasesViewSet(viewsets.ModelViewSet):
    queryset = Bases.objects.all()
    serializer_class = BasesSerializer

class DronesViewSet(viewsets.ModelViewSet):
    queryset = Drones.objects.all()
    serializer_class = DronesSerializer

class StepsViewSet(viewsets.ModelViewSet):
    queryset = Steps.objects.all()
    serializer_class = StepsSerializer

class DeliveriesViewSet(viewsets.ModelViewSet):
    queryset = Deliveries.objects.all()
    serializer_class = DeliveriesSerializer


class LogsViewSet(viewsets.ModelViewSet):
    queryset = Logs.objects.all().order_by('-timestamp')[:10]
    serializer_class = LogsSerializer

