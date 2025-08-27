from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notifications.views  import NotificationView

router = DefaultRouter()
router.register(r'notifications', NotificationView, basename="notification")

urlpatterns = [
    path('', include(router.urls))
]