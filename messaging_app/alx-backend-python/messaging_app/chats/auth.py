from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission

def get_tokens_for_user(user):
    """
    Generate JWT tokens for a given user
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class IsMessageOwner(BasePermission):
    """
    Custom permission to only allow owners of a message to access it
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the sender or receiver of the message
        return obj.sender == request.user or obj.receiver == request.user

class IsConversationParticipant(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        return request.user in [obj.user1, obj.user2]
