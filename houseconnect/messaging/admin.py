from django.contrib import admin
from messaging.models import Messaging
@admin.register(Messaging)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "message", "is_read"]
