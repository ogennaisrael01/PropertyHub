from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ A custom permission to allow user with owner role to create property"""
    def has_object_permission(self, request, view, obj):
        return request.user.role == "Owner"
    
class IsTenant(permissions.BasePermission):
    """ A custom permission to allow user with tenant role to rent property"""
    def has_object_permission(self, request, view, obj):
        return request.user.role == "Tenant"
    
class IsHouseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """ Check if the user is the owner of the house """
        return obj.house.owner == request.user