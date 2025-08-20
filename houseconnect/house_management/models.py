from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class House(models.Model):
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="house_owner"
        )
    title = models.CharField(
        max_length=200, 
        null=False, 
        blank=False)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2) # For purchasing the full building
    location = models.CharField(max_length=200, null=False, blank=False)
    house_type = models.CharField(max_length=100, null=False, blank=False)
    is_available = models.BooleanField(default=False)
    for_rent = models.BooleanField(default=False)
    for_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        """ Returns a URL for house objects """
        return reverse("house", args=str([self.id]))
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]

class HouseImage(models.Model):
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name="house_image"
    )
    caption = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="house_image", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["uploaded_at"]

    def __str__(self):
        if self.caption:
            return self.caption
        return self.house.title
    
class Unit(models.Model):
    """ For getting units that are in one house
    -Eg- Property (Green villa apartment) -- Units (5 units). 
    - each unit can be rented"""
    house = models.ForeignKey(
        House,
        related_name="units",
        on_delete=models.CASCADE
    )
    unit_number = models.CharField(max_length=20)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    living_rooms = models.IntegerField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("unit-detail", args=str([self.id]))
    
    def __str__(self):
        return f"{self.house.title}   Unit {self.unit_number}"
    
class Rental(models.Model):
    tenant = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="rentals"
        )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="rentals"
    )
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        related_name="rentals"
        # For purchasing a full building
    )
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        if self.unit:
            return f"{self.tenant.username} - {self.unit.unit_number}"
        if self.house:
            return f"{self.tenant.username} - {self.house.title}"
        return None
    
    def get_absolut_url(self):
        return reverse("rental_detail", args=str([self.id]))