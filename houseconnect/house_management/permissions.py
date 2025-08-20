from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ A custom permission to allow user with owner role to create property"""
    def has_object_permission(self, request, view, obj):
        return request.user.role == "Owner"