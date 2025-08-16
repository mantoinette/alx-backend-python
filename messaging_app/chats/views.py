from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter  # ✅ Import your filter

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]  # ✅ Enable filtering
    filterset_class = MessageFilter          # ✅ Use custom filter

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        conversation_id = conversation.id
        user = self.request.user

        if user not in conversation.participants.all():
            return Response(
                {"detail": "Hello, please You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=user)
