from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of a message/conversation to view or edit it
    """
    def has_object_permission(self, request, view, obj):
        # Admin permissions
        if request.user.is_staff:
            return True
            
        # Check if the object has a user field directly
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        # For conversations, check if user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
            
        return False
        