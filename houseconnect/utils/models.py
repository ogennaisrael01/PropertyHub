from django.db import models
from django.conf import settings
from house_management.models import House

class Messages(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="messages"
        )
    reciever = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="messages",
        on_delete=models.CASCADE
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    house = models.ForeignKey(
        House, 
        on_delete=models.DO_NOTHING,
        related_name="messages"
    )

