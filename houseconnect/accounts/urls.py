from django.urls import path, include
from accounts.views import (
    RegistrationView,
    ProfileView)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

router = DefaultRouter()
router.register(r'profile', ProfileView)

app = "accounts"
urlpatterns = [
    path("accounts/", include(router.urls)),
    path("accounts/register/", RegistrationView.as_view(), name="register"),
    # path("auth/", include("rest_framework.urls")),
    path("accounts/login/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("accounts/logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
]