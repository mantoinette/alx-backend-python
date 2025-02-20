from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

class Message(MPTTModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)  # Track if message has been edited
    last_edited = models.DateTimeField(null=True, blank=True)  # When it was last edited
    
    # Add parent_message field for threaded conversations
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    class MPTTMeta:
        order_insertion_by = ['timestamp']

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"

    @property
    def thread_messages(self):
        """Get all messages in the thread efficiently"""
        return (
            Message.objects
            .filter(tree_id=self.tree_id)
            .select_related('sender', 'receiver')
            .prefetch_related('history')
            .order_by('tree_id', 'lft')
        )

    """
    Example usage of threaded messages:
    
    # Get a message and all its replies efficiently
    message = Message.objects.get(id=1)
    thread = message.thread_messages

    # Get direct replies to a message
    direct_replies = message.replies.all()

    # Get the parent message
    parent = message.parent

    # Get the root message of a thread
    root_message = message.get_root()

    # Get all descendants (replies) of a message
    all_replies = message.get_descendants()
    """

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()  # Store the previous content
    edited_at = models.DateTimeField(auto_now_add=True)  # When the edit was made
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Who made the edit

    class Meta:
        ordering = ['-edited_at']  # Most recent edits first

    def __str__(self):
        return f"Edit history for message {self.message.id} at {self.edited_at}"
