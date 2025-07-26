from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Return only messages where the user is a participant in the conversation.
        """
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user)
