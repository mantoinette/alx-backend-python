from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants to send/view/update/delete messages in a conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the request is a read or write operation
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()
        return False
