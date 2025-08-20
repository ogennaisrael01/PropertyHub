from django.urls import path, include
from accounts.views import (
    RegistrationView,
    UserListApiView,
    ProfileAPIView,
    ProfileRetrieveApiView,
    ProfileUpdateApiView,
    ProfileDeleteApiView,

    
)
app = "accounts"
urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("users/", UserListApiView.as_view(), name="users"),
    path("profile/<int:pk>/", ProfileAPIView.as_view(), name="user_profile"),
    path("profile/<int:pk>/retrieve/", ProfileRetrieveApiView.as_view(), name="profile_retrieve"),
    path("profile/<int:pk>/update/", ProfileUpdateApiView.as_view(), name="profile_update"),
    path("profile/<int:pk>/delete/", ProfileDeleteApiView.as_view(), name="profile_delete"),
    path("auth/", include("rest_framework.urls")),

]