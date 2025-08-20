from django.urls import path
from house_management.views import (
    HouseCreateApiView,
    HouseListApiView,
    HouseDeleteApiView,
    HouseRetrieveApiView,
    HouseUpdateApiView,
    UnitCreateApiView,
    UnitListApiView,
    UnitRetrieveUpdateDestroyApiView


)

app = "house_management"
urlpatterns = [
    path("house/create/", HouseCreateApiView.as_view(), name="house_create"),
    path("house/list/", HouseListApiView.as_view(), name="house_detail"),
    path("house/<int:pk>/update/", HouseUpdateApiView.as_view(), name="house_update"),
    path("house/<int:pk>/delete/", HouseDeleteApiView.as_view(), name="house_delete"),
    path("house/<int:pk>/retrieve/", HouseRetrieveApiView.as_view(), name="house_retrieve"),
    path("house/<int:pk>/unit/create", UnitCreateApiView.as_view(), name="create_unit"),
    path("house/units/", UnitListApiView.as_view(), name="list_units"),
    path("house/unit/<int:pk>/detail/", UnitRetrieveUpdateDestroyApiView.as_view(), name="unit-detail")
]