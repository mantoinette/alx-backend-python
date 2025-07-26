from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

class MessageViewSet(viewsets.ModelViewSet):
    ...
    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        user = self.request.user

        # Check if user is a participant
        if user not in conversation.participants.all():
            raise PermissionDenied(detail="Hello?, You are not a participant in this conversation.")

        serializer.save(sender=user)
