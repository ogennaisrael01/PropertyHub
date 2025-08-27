from rest_framework import serializers
from accounts.serializers import UserProfileSerializer
from messaging.models import Messaging

class MessagingSerializer(serializers.ModelSerializer):
    sender_profile = UserProfileSerializer(read_only=True)
    receiver_profile = UserProfileSerializer(read_only=True)
   
    
    class Meta:
        model = Messaging
        fields = ["id", "sender", "receiver", "sender_profile", "receiver_profile", "message", "date_created"]
        read_only_fields = ["sender", "id", "date_created"]