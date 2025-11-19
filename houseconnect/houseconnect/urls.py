
from django.contrib import admin
from django.urls import path, include


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import  openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="API documentation for my travel app",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="ogennaisrael98@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path("", include("house_management.urls")),
    path("", include("accounts.urls")),
    path("", include("notifications.urls")),
    path("", include("messaging.urls")),
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
