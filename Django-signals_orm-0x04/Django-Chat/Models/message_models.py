from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)  # Track if message has been edited
    last_edited = models.DateTimeField(null=True, blank=True)  # When it was last edited

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()  # Store the previous content
    edited_at = models.DateTimeField(auto_now_add=True)  # When the edit was made
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Who made the edit

    class Meta:
        ordering = ['-edited_at']  # Most recent edits first

    def __str__(self):
        return f"Edit history for message {self.message.id} at {self.edited_at}"
