from rest_framework import serializers
from house_management.models import House, Unit
from django.utils import timezone



class UnitSerializer(serializers.ModelSerializer):
    # house = serializers.PrimaryKeyRelatedField(queryset=House.objects.all())
    url = serializers.SerializerMethodField
    class Meta:
        model = Unit
        fields = ["url", "unit_number", "bedrooms", "bathrooms", "living_rooms", "rent_amount", "is_available"]

    def get_url(self, obj):
        return obj.get_absolute_url()

class HouseSerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(read_only=True, view_name="user_profile")
    date_uploaded = serializers.SerializerMethodField()
    units = UnitSerializer(many=True, read_only=True)
    class Meta:
        model = House
        fields = ["id", "owner", "title", "description", "price", "location", "house_type",\
                 "is_available", "for_rent", "for_sale", "date_uploaded", "units"]
    

    def get_date_uploaded(self, obj):
        """ Returns the how long the house has been uploaded"""
        now = timezone.now()
        if obj.created_at:
            delta = now - obj.created_at
            return f"{delta.days} day(s) ago"
        return None