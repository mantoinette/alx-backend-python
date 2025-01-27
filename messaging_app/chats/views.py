from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, CustomUserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        """
        participant_ids = request.data.get("participant_ids", [])
        if len(participant_ids) < 2:
            return Response(
                {"error": "A conversation must have at least two participants."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        """
        Send a message to an existing conversation.
        """
        conversation = get_object_or_404(Conversation, pk=pk)
        sender_id = request.data.get("sender_id")
        message_body = request.data.get("message_body")

        if not sender_id or not message_body:
            return Response(
                {"error": "Both sender_id and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message = Message.objects.create(
            sender_id=sender_id,
            conversation=conversation,
            content=message_body,
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and retrieving messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Prevent direct message creation; messages should only be created via a conversation.
        """
        return Response(
            {"error": "Messages must be created via a conversation."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
