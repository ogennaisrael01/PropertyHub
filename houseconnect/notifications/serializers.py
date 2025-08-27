from rest_framework import serializers
from notifications.models import Notification
class NotificationSeerializer(serializers.ModelSerializer):
    reciever = serializers.CharField(source="reciever.email")
    class Meta:
        model = Notification
        fields = ["reciever", "content", "created_at", "read"]