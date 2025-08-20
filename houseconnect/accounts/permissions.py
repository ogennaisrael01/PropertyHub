from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    # Allow users to edit their own profiles
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user