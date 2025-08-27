from django.db import models
from django.conf import settings

class Notification(models.Model):
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification")
    read = models.BooleanField(default=False)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Notification for {self.reciever}: {self.content}"
