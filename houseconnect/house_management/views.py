from django.shortcuts import render
from house_management.serializers import HouseSerializer, UnitSerializer, RentalSerializer, ImageSerializer
from house_management.models import House, Unit, Rental, HouseImage
from rest_framework import status, filters, permissions, viewsets, mixins
from rest_framework.response import Response
from house_management.permissions import IsOwner, IsTenant, IsHouseOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.pagination import PageNumberPagination



class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = page_size
    max_page_size = 20

# API view for House management
class HouseManagementViewset(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields  = ["price", "location"]
    search_fields = ["price", "location", "units__bedrooms", "units__bathrooms", "units__living_rooms"]

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """ Allow only users with Owner role to create a property"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            Notification.objects.create(
                reciever=request.user,
                content="You uploaded a house"
            )
            send_mail(subject="House uploads",
                    from_email= settings.DEFAULT_FROM_EMAIL,
                    message=f"Hello {request.user.username}, We are reaching out to inform that your house uploads was successfull and you will be notified when tenants starts to request for your property",
                    recipient_list=[request.user.email],
                    fail_silently=False)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "msg": f"Error: {e}"})
        serializer.save(owner=request.user)
        return Response(data={"success": True, "data": serializer.validated_data}, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        queryset = self.get_queryset()
        if queryset:
            queryset = queryset.filter(is_available=True).order_by("-created_at")
        serializer = self.get_serializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data={"success": True, "data": serializer.data})
    
class UnitManagementView(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPageNumberPagination
    filterset_fields = ["unit_number", "bedrooms", "bathrooms", "rent_amount", "living_rooms"]

   
    def get_permissions(self):
       if self.action in ["create", "update", "destroy", "partial_update"]:
           permission_classes = [permissions.IsAuthenticated, IsHouseOwner]
       else:
           permission_classes = [permissions.AllowAny]
       return [perm() for perm in permission_classes]

    def create(self, request, *args, **kwargs):
        house_id = self.kwargs.get("house_pk")
        house = get_object_or_404(House, house_id=house_id)
        if request.user != house.owner:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"success": False, "msg": "You are not authorized to perfrom this action"})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




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
            # notify the house owner that a rental has been intiated
            Notification.objects.create(
                receiver=self.get_house_object().owner,
                content=f"{request.user} has requested for {self.get_house_object().house_type} in {self.get_house_object().location} "
            ) 
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
            
            # notify the house owner that a rental has been intiated
            Notification.objects.create(
                receiver=self.get_house_object().owner,
                content=f"{request.user} has requested for unit in {self.get_house_object().location}: Unit number {self.get_unit_object().unit_number}"
            ) 
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
    

    