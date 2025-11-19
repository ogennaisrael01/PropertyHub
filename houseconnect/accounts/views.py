
from rest_framework import  generics, permissions, viewsets, status
from accounts.serializers import (
    RegistrationSerializer, 
    UserProfileSerializer, 
    CustomTokenObtainPairSerializer,
    AvaterSerializer,
)
from django.contrib.auth import get_user_model
from accounts.models import Profile, Avater
from accounts.permissions import IsOwner
from rest_framework.response import Response
from rest_framework.decorators import action
from notifications.models import Notification
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()
class RegistrationView(generics.CreateAPIView):
    """ Handle user registration """

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.validated_data.pop("password")
        return Response(status=status.HTTP_201_CREATED, data={"success": True, "data": serializer.validated_data})

    
class ProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.select_related("user")
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_permissions(self):
        if  self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        elif self.action in ["list"]:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [perm() for perm in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """ Create a user profile """
        if Profile.objects.filter(user=request.user).exists():
            return Response({"Message": "Already have a profile."})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        message = "Profile  objects created successfully"
        try:
            Notification.objects.create(
                reciever=request.user,
                content=message
                )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "mgs": f"Error occured: {e}"})
        return Response(serializer.validated_data)
       
        
    @action(methods=["get"], detail=False, url_path="Me")
    def get_loggedin_user_profile(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        serializer = self.get_serializer(profile)
        return Response(status=status.HTTP_200_OK, data={"success": True, "data": serializer.data})

class CustomTokenObtainPaiView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

class AvaterViewset(viewsets.ModelViewSet):
    queryset = Avater.objects.all()
    serializer_class = AvaterSerializer
    permission_classes  = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
    