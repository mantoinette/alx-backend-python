from rest_framework import viewsets
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# ViewSet for handling conversations
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        # Custom logic to create a conversation
        return super().create(request, *args, **kwargs)

# ViewSet for handling messages in a specific conversation
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        conversation = self.get_object()  # Fetch the conversation
        # Add custom logic for creating messages related to the conversation
        return super().create(request, *args, **kwargs)
