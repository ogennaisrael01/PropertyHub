from django.shortcuts import render
from rest_framework import  generics
from rest_framework import permissions
from accounts.serializers import RegistrationSerializer, UserOutputSerilializer, UserProfileSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.models import Profile
from accounts.permissions import IsOwner
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action

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
    
class ProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()
    def get_permissions(self):
        if self.action in ["create", "destroy", "update", "partial_update"]:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        elif self.action == "get_profile":
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == "retrieve":
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [perm() for perm in permission_classes]

    def create(self, request, *args, **kwargs):
        """ Create a user profile """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return None
        
    def update(self, request, *args, **kwargs):
        """" Update a user profile """
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return None
    
    def partial_update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return None
    
    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile:
            profile.delete()
            return Response({"Detail": "Profile deleted"})
        else:
            return Response({"Detail": "Can't delete prpofile"})

    @action(methods=["get"], detail=False, url_path="me")
    def get_profile(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"Message": "No Profile Created"})
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    