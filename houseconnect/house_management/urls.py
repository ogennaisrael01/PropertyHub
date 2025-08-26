from django.urls import path, include
from house_management.views import (
    HouseManagementViewset,
    UnitManagementView,
    RentHouseManagementView,
    RentUnitManagementView,
    RentalListApiView,
    ImageView
)
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'houses', HouseManagementViewset, basename="houses")
router.register(r"rentals", RentalListApiView, basename="rentals")


# URL for units under house (Nested)
house_router = routers.NestedDefaultRouter(router, r'houses', lookup='house')
house_router.register(r'units', UnitManagementView, basename='house-units')
house_router.register(r"rentals", RentHouseManagementView, basename="house-rental")
house_router.register(r'images', ImageView, basename="images")

# URL for renting a unit under a  house (Nested)
unit_router = routers.NestedDefaultRouter(house_router, r'units', lookup='unit')
unit_router.register(r"rentals", RentUnitManagementView, basename="unit-rental")

app = "house_management"
urlpatterns = [
    path("", include(router.urls)),
    path('', include(house_router.urls)),
    path('', include(unit_router.urls))
]