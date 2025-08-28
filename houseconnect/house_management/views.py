from django.shortcuts import render
from house_management.serializers import HouseSerializer, UnitSerializer, RentalSerializer, ImageSerializer
from house_management.models import House, Unit, Rental, HouseImage
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from house_management.permissions import IsOwner, IsTenant, IsHouseOwner
from rest_framework.exceptions import NotFound, PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from notifications.models import Notification


# API view for House management
class HouseManagementViewset(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields  = ["price", "location"]
    search_fields = ["price", "location", "units__bedrooms", "units__bathrooms", "units__living_rooms"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ["create", "update", "destroy", "partial_update"]:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """ Allow only users with Owner role to create a property"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            Notification.objects.create(
                reciever=request.user,
                content="You uploaded a house"
            )
            return Response({"Detail": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Detail": "Data not valid"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        """ A queryset to list all houese that are available """
        return House.objects.filter(is_available=True).order_by("-created_at")
        

    def update(self, request, *args, **kwargs):
        house = self.get_object()
        if house:
            serializer = self.get_serializer(house, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(owner=request.user)
                return Response(serializer.data)
        return house.objects.none()
    
    def destroy(self, request, *args, **kwargs):
        house = self.get_object()
        try:
            house.delete()        
        except House.DoesNotExist:
            return Response({"Message": "House not found"})
        return Response({"Message": f"{house} Deletes"})
    
    def partial_update(self, request, *args, **kwargs):
        house = self.get_object()
        if house:
            serializer = self.get_serializer(house, data-request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(owner=request.user)
                return Response(serializer.data)
        else:
            return house.objects.none()
        

class UnitManagementView(mixins.ListModelMixin,
                         viewsets.GenericViewSet,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["unit_number", "bedrooms", "bathrooms", "rent_amount", "living_rooms"]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
   
    def get_permissions(self):
       if self.action in ["create", "update", "destroy", "partial_update"]:
           permission_classes = [permissions.IsAuthenticated, IsHouseOwner]
       else:
           permission_classes = [permissions.IsAuthenticatedOrReadOnly]
       return [perm() for perm in permission_classes]

    def get_house_object(self):
        return get_object_or_404(House, id=self.kwargs["house_pk"])
    
    def get_queryset(self):
        """ A query set to list all avilable units under the given house """
        queryset = Unit.objects.all()
        if queryset.exists() and self.get_house_object():
            return queryset.filter(house=self.get_house_object(), is_available=True)
        else:
            return Unit.objects.none()
    
    @action(methods=["post"], url_path="create", detail=False)
    def create_unit(self, request, *args, **kwargs):
        # Only the owner of the house can create units for it
        if self.get_house_object() and self.get_house_object().owner == request.user:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(house=self.get_house_object())
                return Response({"Detail": "Unit created", "Data": serializer.data}, status=status.HTTP_201_CREATED)  
    
    def update(self, request, *args, **kwargs):
        unit = self.get_object()
        if unit and self.get_house_object() and self.get_house_object().owner == request.user:
            serializer = self.get_serializer(unit, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(house=self.get_house_object())
                return Response({"Message": "Updated", "Data": serializer.data})


class RentHouseManagementView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RentalSerializer
    queryset = Rental.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    
    def get_house_object(self):
        house_id = self.kwargs["house_pk"]
        house = get_object_or_404(House, id=house_id)
        return house
    
    def create(self, request, *args, **kwargs):
        """ Create a rental for a house"""
        serializer = self.get_serializer(data=request.data)
    
        if  self.get_house_object() and serializer.is_valid(raise_exception=True):
            serializer.save(tenant=self.request.user, house=self.get_house_object())
            return Response({"Rented": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Detail": "Rental With Invalid Credential"})

class RentUnitManagementView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RentalSerializer
    queryset = Rental.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_unit_object(self):
        return get_object_or_404(Unit, id=self.kwargs["unit_pk"])
    
    def get_house_object(self):
        return get_object_or_404(House, id=self.kwargs["house_pk"])
    
    def create(self, request, *args, **kwargs):
        """Create a rental for a unit"""
        serializer = self.get_serializer(data=request.data)
        
        if  self.get_unit_object() and serializer.is_valid(raise_exception=True):
            serializer.save(tenant=self.request.user, house=self.get_house_object(), unit=self.get_unit_object())
            return Response({"Detail": True, "Data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Detail": "Rental With Invalid Credential"})

# APi for handling retreival of rentals made by a tenent
class RentalListApiView(viewsets.GenericViewSet):
        serializer_class = RentalSerializer
        permission_classes = [permissions.IsAuthenticated]

        @action(methods=["get"], detail=False, url_path="my_rentals")
        def get_rentals(self, request, *args, **kwargs):
            """ rentals made by tenant (current user)"""
            try:
                rentals = Rental.objects.select_related("tenant").filter(tenant=request.user)
            except Rental.DoesNotExist:
                return Response({"Detail": "No rentals made"})
            serializer = self.get_serializer(rentals, many=True)
            return Response(serializer.data)
        

class ImageView(viewsets.GenericViewSet):
    serializer_class = ImageSerializer
    queryset = HouseImage.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsHouseOwner]

    @action(methods=["post"], url_path="create", detail=False)
    def create_image(self, request, *args, **kwargs):
        house = get_object_or_404(House, id=self.kwargs["house_pk"])
        if house and house.owner == request.user:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(house=house)
                return Response(serializer.data)
            else:
                return Response({"Invalid": "Invalid"})
        return Response({"Message": "Can't create image"})

    @action(methods=["delete"], detail=True, url_path="delete")  
    def delete_image(self, request, *args, **kwargs):
        house = get_object_or_404(House, id=self.kwargs["house_pk"])
        instance = self.get_object()
        try:
            if house and house.owner == request.user:
                instance.delete()
        except House.DoesNotExist or instance is None:
            return Response({"Message": "No data found"})
        return Response({"Message": "Image deleted"})
    

    