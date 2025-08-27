from django.shortcuts import render
from rest_framework import viewsets, mixins
from messaging.serializers import MessagingSerializer
from messaging.models import Messaging
from django.contrib.auth import get_user_model
from django.db.models import Q, Subquery
from rest_framework.decorators import action
from rest_framework.response import Response  
from django.shortcuts import get_object_or_404  
User = get_user_model()

class MessagingView(viewsets.GenericViewSet, 
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin):
    """ Retrieve all messages between a sender and a reciever """
    serializer_class = MessagingSerializer
    queryset = Messaging.objects.all()

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs["pk"])


    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        other_user = self.get_object()
        messages = Messaging.objects.filter(
                                        Q(sender=user, receiver=other_user) |
                                        Q(receiver=user, sender=other_user)
        ).order_by("-date_created")
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """create message and save the login user as the sender """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(sender=request.user)
            return Response(serializer.data)