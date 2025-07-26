# chats/permissions.py

from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only owners to access their own messages or conversations.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.sender == request.user or obj.receiver == request.user
