from django.shortcuts import render
from rest_framework import viewsets
from notifications.serializers import NotificationSeerializer
from notifications.models import Notification
from rest_framework.decorators import action
from rest_framework.response import Response
from notifications.permissions import IsOwner
from rest_framework import permissions

class NotificationView(viewsets.GenericViewSet):
    serializer_class = NotificationSeerializer
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    @action(methods=["get"], detail=False)
    def get_notifications(self, request, *args, **kwargs):
        user = request.user
        try:
            notification = Notification.objects.filter(reciever=user).all().order_by("-created_at")[:5]
        except Notification.DoesNotExist:
            return Response({"Message": "No Notification"})
        serializer = self.get_serializer(notification, many=True)
        return Response(serializer.data)
    
    @action(detail=True, url_path="mark_as_read")
    def mark_as_read(self, request, *args, **kwargs):
        notification = self.get_object()

        try:
            if notification.reciever == request.user and notification.read != True:
                notification.read = True
                notification.save()
            else:
                return Response({"Message": "Already marked as read"})
        except Notification.DoesNotExist:
            return Response({"Message": "Not found"})
        return Response({"Message": "marked as read"})