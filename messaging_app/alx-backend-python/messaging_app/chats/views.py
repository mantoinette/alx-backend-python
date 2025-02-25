from rest_framework import viewsets, status, filters  # Import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .auth import IsMessageOwner, IsConversationParticipant


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Add filters
    search_fields = ["participants__username"]  # Search by participant username
    ordering_fields = ["created_at", "updated_at"]  # Order by timestamps
    permission_classes = [IsAuthenticated, IsConversationParticipant]

    def create(self, request, *args, **kwargs):
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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Add filters
    search_fields = ["sender__username", "conversation__id"]  # Search by sender or conversation
    ordering_fields = ["created_at"]  # Order by creation time
    permission_classes = [IsAuthenticated, IsMessageOwner]

    def create(self, request, *args, **kwargs):
        return Response(
            {"error": "Messages must be created via a conversation."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

@login_required
@cache_page(60)  # Cache for 60 seconds
def conversation_messages(request, conversation_id):
    """Display messages in a conversation"""
    messages = (
        Message.objects
        .filter(conversation_id=conversation_id)
        .select_related('sender')
        .order_by('timestamp')
    )
    
    messages_data = [{
        'id': msg.id,
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp.isoformat(),
        'is_read': msg.is_read
    } for msg in messages]
    
    return JsonResponse({
        'conversation_id': conversation_id,
        'messages': messages_data
    })

@login_required
def send_message(request, conversation_id):
    """Send a new message (not cached)"""
    if request.method == 'POST':
        content = request.POST.get('content')
        message = Message.objects.create(
            conversation_id=conversation_id,
            sender=request.user,
            content=content
        )
        return JsonResponse({
            'status': 'success',
            'message_id': message.id
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
