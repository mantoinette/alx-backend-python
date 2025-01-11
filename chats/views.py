from django.shortcuts import render
from rest_framework import response
from .models import Conversation ,Message
from . serializer import ConversationSerializer, MessageSerializer


# Create your views here.
class conversationViewSet(Viewset.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationViewSet
    
    def create(self, request, *args, **kwargs):
        # Create a serializer instance with the data from the request
     serializer = self.get_serializer(data=request.data)
    -
    # Check if the serializer data is valid
    if serializer.is_valid():
        # Save the new instance to the database
        serializer.save()
        # Return a response with the serialized data and a 201 Created status
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # If the data is not valid, return the errors with a 400 Bad Request status
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

Class MessageViewSet(ViewSet.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class =  messageViewSet   
    
    def create(self, request, *args, **kwags):
        serializer = self.get.serializeR(data = request.data)
        if serializer.is_valid():
            return response(serializer.data status = status.http_201_created)
        return response(serializer.error, status = status.Http_400_Bad_request)
        
 