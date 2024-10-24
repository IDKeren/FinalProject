from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PickupLocationsViewSet, DropLocationsViewSet,ObstaclesViewSet, LogsViewSet,BasesViewSet, DronesViewSet, StepsViewSet, DeliveriesViewSet

drones_router = DefaultRouter()
drones_router.register(r'', DronesViewSet)

bases_router = DefaultRouter()
bases_router.register(r'', BasesViewSet)

drops_router = DefaultRouter()
drops_router.register(r'', DropLocationsViewSet)

pickups_router = DefaultRouter()
pickups_router.register(r'', PickupLocationsViewSet)

obstacles_router = DefaultRouter()
obstacles_router.register(r'', ObstaclesViewSet)

logs_router = DefaultRouter()
logs_router.register(r'', LogsViewSet)

urlpatterns = [
    path('drones', include(drones_router.urls)),
    path('bases', include(bases_router.urls)),
    path('obstacles', include(obstacles_router.urls)),
    path('pickups', include(pickups_router.urls)),
    path('drops', include(drops_router.urls)),
    path('logs', include(logs_router.urls))
]