from django.contrib import admin
from house_management.models import House, Unit, Rental


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ["owner__email", "title", "price", "is_available"]
    list_filter = ["price", "is_available"]

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["house__title", "unit_number", "is_available"]
    list_filter = ["bedrooms", "bathrooms", "rent_amount", "is_available"]

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ["tenant__email", "unit__unit_number", "house__title", "amount"]