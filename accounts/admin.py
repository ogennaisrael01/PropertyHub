from django.contrib import admin
from accounts.models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["email", "date_joined", "is_staff"]
