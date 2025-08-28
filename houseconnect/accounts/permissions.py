from rest_framework import permissions

class IsOwner(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
        print(f"Debug: {request.user} {obj.user}")
        return obj.user == request.user