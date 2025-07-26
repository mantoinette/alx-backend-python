from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Show only messages where the user is a participant
        return Message.objects.filter(
            sender=self.request.user
        ) | Message.objects.filter(
            receiver=self.request.user
        )
