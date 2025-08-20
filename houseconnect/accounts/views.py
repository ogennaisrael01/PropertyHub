from django.shortcuts import render
from rest_framework import  generics
from rest_framework import permissions
from accounts.serializers import RegistrationSerializer, UserOutputSerilializer, UserProfileSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.models import Profile
from accounts.permissions import IsOwner
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

User = get_user_model()

class RegistrationView(generics.CreateAPIView):
    """ Handle user registration """

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Detail": "User Registration Successful"})
        else:
            return Response({"Detail": "Credentials not valid"})
        
    
class UserListApiView(generics.ListAPIView):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserOutputSerilializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["username", "role"]
    search_fields = ["role", "user_profile__address"]

class ProfileAPIView(generics.ListCreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """ Get the profile for the current user """
        user = self.request.user
        # Unauthenticated users cant access profile page
        if not user.is_authenticated:
            return Profile.objects.none()
        # Staff users can view all users profile
        if user.is_staff:
            return Profile.objects.all()
        
        return Profile.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        serailizer = self.get_serializer(data=request.data)

        # validate serializer
        if serailizer.is_valid(raise_exception=True):
            serailizer.save(user=self.request.user)
            return Response({"Detail": "Profile created successful"}, status=201)
        return Response({"Detail": "Profile Error"}, status=400)

class ProfileRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        """ User can only retrieve their own profile but admins can retrieve all user profile """

        user = self.request.user
        if user.is_staff:
            return Profile.objects.all()
        else:
            return Profile.objects.get(user=user)
        
class ProfileUpdateApiView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_object(self):
        """ Users can only edit their post"""

        profile = Profile.objects.get(pk= self.kwargs["pk"])
        if profile.user != self.request.user:
            raise PermissionDenied({"Detail": "Dont have access to edit other users post"})
        
        return profile
    

class ProfileDeleteApiView(generics.DestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """ Users can only edit their post"""

        profile = Profile.objects.get(pk= self.kwargs["pk"])
        if profile.user != self.request.user:
            raise PermissionDenied({"Detail": "Dont have access to delete other users post"})
        
        return profile

    def perform_destroy(self, instance):
        instance.delete()
        return Response({"Detail": "Profile deleted Successful"})
