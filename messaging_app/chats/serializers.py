from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class CustomUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)  # Include full name as a calculated field

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "profile_photo",
            "bio",
            "full_name",
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)  # Include sender's username
    time_sent = serializers.SerializerMethodField()  # Custom method field to format the sent_at timestamp

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "sender_username",
            "conversation",
            "message_body",
            "time_sent",
        ]

    def get_time_sent(self, obj):
        return obj.sent_at.strftime("%Y-%m-%d %H:%M:%S")  # Format the timestamp for readability


class ConversationSerializer(serializers.ModelSerializer):
    participants = CustomUserSerializer(many=True, read_only=True)  # Include participant details
    messages = MessageSerializer(many=True, read_only=True, source="messages")  # Include nested messages
    total_messages = serializers.SerializerMethodField()  # Custom method field to count messages

    class Meta:
        model = Conversation
        fields = [
            "id",
            "participants",
            "messages",
            "total_messages",
            "created_at",
            "updated_at",
        ]

    def get_total_messages(self, obj):
        return obj.messages.count()  # Count the number of messages in the conversation


# Custom Validation Example
class ConversationCreateSerializer(serializers.Serializer):
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )

    def validate_participant_ids(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return value
