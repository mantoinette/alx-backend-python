from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """Get all unread messages for a specific user"""
        return (
            self.get_queryset()
            .filter(
                receiver=user,
                is_read=False
            )
            .select_related('sender')
            .only(
                'id',
                'sender__username',
                'content',
                'timestamp'
            )
            .order_by('-timestamp')
        )

    def mark_as_read(self, message_ids, user):
        """Mark multiple messages as read for a user"""
        return (
            self.get_queryset()
            .filter(
                id__in=message_ids,
                receiver=user,
                is_read=False
            )
            .update(is_read=True)
        )
