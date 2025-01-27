from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "profile_photo",
            "bio",
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)  # Nest user details within the message

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "conversation",
            "message_body",
            "sent_at",
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = CustomUserSerializer(many=True, read_only=True)  # Include participant details
    messages = MessageSerializer(many=True, read_only=True, source="messages")  # Include messages within conversation

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
            "updated_at",
        ]
