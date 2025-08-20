from django.shortcuts import render
from house_management.serializers import HouseSerializer, UnitSerializer
from house_management.models import House, Unit
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from house_management.permissions import IsOwner
from rest_framework.exceptions import NotFound, PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class HouseCreateApiView(generics.CreateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def create(self, request, *args, **kwargs):
        """ Allow only users with Owner role to create a property"""

        if self.request.user.role != "Owner":
            return Response(
                {"Detail": f"Can't create property with {self.request.user.role} role. \
                Create account with Owner role to create poperty"},
                status=status.HTTP_403_FORBIDDEN
                )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=self.request.user)
            return Response({"Detail": "Property created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Detail": "Data not valid"}, status=status.HTTP_400_BAD_REQUEST)
    
class HouseListApiView(generics.ListAPIView):
    serializer_class = HouseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["price", "location"]
    search_fields = ["price", "location", "units__bedrooms", "units__bathrooms", "units__living_rooms"]
    

    def get_queryset(self):
        """ Returns all Property which are available else Notify that no record was found"""
        queryset = House.objects.all()
        is_available = True
        if queryset:
            queryset.filter(is_available=is_available)
                
        else:
            raise NotFound({"Detail": "No Record found"})

        return queryset

class HouseUpdateApiView(generics.UpdateAPIView):
    serializer_class = HouseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_object(self):
        house = House.objects.get(pk=self.kwargs["pk"])
        if house.owner != self.request.user or self.request.user.role != "Owner" or self.request.user.is_staff == False:
            raise  PermissionDenied({"Detail": "Can't UPdate this Property"})  

        return house
    
class HouseRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = HouseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """ admins users can view all users property """
        queryset = House.objects.all()
        return queryset
    
class HouseDeleteApiView(generics.DestroyAPIView):
    serializer_class = HouseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        house = House.objects.get(pk=self.kwargs["pk"])
        if house.owner != self.request.user or self.request.user.role != "Owner" or self.request.user.is_staff == False:
            raise  PermissionDenied({"Detail": "Can't Delete this Property"})  

        return house
    def perform_destroy(self, instance):
        instance.delete()
        return Response({"Detail": "Property deleted"})


class UnitCreateApiView(generics.CreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):

        house_id = self.kwargs["pk"]  # Get the house ID from the URL
        house = House.objects.get(pk=house_id)  # Get the house object

        if house.owner != self.request.user or self.request.user.role != "Owner":  # Check if the user is the owner
            return Response({"Detail": "Cant create units for other users property"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(house=house)  # Save the unit with the associated house
            return Response({"Detail": "Unit created"}, status=status.HTTP_201_CREATED) # Send successful message
        
class UnitListApiView(generics.ListAPIView):
    serializer_class = UnitSerializer
    permission_classes  = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["unit_number", "bedrooms", "bathrooms", "rent_amount", "living_rooms"]
    def get_queryset(self):
        queryset = Unit.objects.all()
        # Show available units for rent
        available = True
        return queryset.filter(is_available=available)
    
class UnitRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        """ get the unit object"""
        unit_id = self.kwargs["pk"]
        unit = Unit.objects.get(pk=unit_id)
        return unit
    
    def perform_update(self, serializer):
        # Only the person that created the unit can update it
        if self.get_object().house.owner != self.request.user or self.request.user.role != "Owner":
            raise PermissionDenied({"Detail": "Cant update unit that you did not create"})
        serializer.save(hoouse=self.get_object().house)

    def perform_destroy(self, instance):
        if self.get_object().house.owner != self.request.user or self.request.user.role != "Owner":
            raise PermissionDenied({"Detail": "Cant delete unit that you did not create"})
        instance.delete()
        return Response({"Detail": "Unit deleted"})
    
    def get_queryset(self):
        return super().get_queryset()
        