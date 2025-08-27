from django.urls import path, include
from rest_framework.routers import DefaultRouter
from messaging.views import MessagingView

router = DefaultRouter()
router.register(r'messages', MessagingView, basename="messages")

urlpatterns = [
    path("", include(router.urls))
]