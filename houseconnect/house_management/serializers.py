from rest_framework import serializers
from house_management.models import House, Unit, Rental, HouseImage
from django.utils import timezone
from accounts.serializers import UserOutputSerilializer



class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "unit_number", "bedrooms", "bathrooms", "living_rooms", "rent_amount", "is_available"]

    def create(self, validated_data):
        return Unit.objects.create(**validated_data)

class ImageSerializer(serializers.ModelSerializer):
    house = serializers.ReadOnlyField(source="house.title")
    class Meta:
        model = HouseImage
        fields = ["id", "house", "image", "uploaded_at", "caption"]    

class HouseSerializer(serializers.ModelSerializer):
    owner = UserOutputSerilializer(read_only=True)
    date_uploaded = serializers.SerializerMethodField()
    units = UnitSerializer(many=True, read_only=True)
    image = ImageSerializer(source="house_image", read_only=True, many=True)

    class Meta:
        model = House
        fields = ["id", "owner", "title", "description", "price", "location", "house_type",\
                 "is_available", "for_rent", "for_sale", "date_uploaded", "units", "image"]
    

    def get_date_uploaded(self, obj):
        """ Returns the how long the house has been uploaded"""
        now = timezone.now()
        if obj.created_at:
            delta = now - obj.created_at
            return f"{delta.days} day(s) ago"
        return None
    
class RentalSerializer(serializers.ModelSerializer):
    house = serializers.ReadOnlyField(source="house.title")
    tenant = serializers.ReadOnlyField(source="tenant.username")
    unit = serializers.ReadOnlyField(source="unit.unit_number")

    class Meta:
        model = Rental
        fields = ["id", "house", "tenant", "unit", "start_date", "end_date", "date_created", "amount", "is_active"]


    def validate(self, data):
        """ validate that the start can be anything less than today"""
        if data["start_date"] < timezone.now().date():
            raise serializers.ValidationError("Start date can't be less than today")
        
        if data["end_date"] < data["start_date"]:
            raise serializers.ValidationError("End date can't occur before start")
        return data

    def create(self, validated_data):
        return Rental.objects.create(**validated_data)


    