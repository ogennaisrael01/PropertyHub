from django.urls import path, include
from accounts.views import (
    RegistrationView,
    ProfileView,
    CustomTokenObtainPaiView,
    AvaterViewset
    )
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

router = DefaultRouter()
router.register(r'profile', ProfileView, basename="profile")
router.register(r'avater', AvaterViewset, basename="picture")

app = "accounts"
urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", CustomTokenObtainPaiView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
]