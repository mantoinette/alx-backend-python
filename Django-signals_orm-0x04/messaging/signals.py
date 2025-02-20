from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import transaction, models
from django.utils import timezone
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:  # Only create notification for new messages
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal to clean up all user-related data after account deletion
    with explicit cleanup and logging
    """
    try:
        with transaction.atomic():
            # Delete all messages
            Message.objects.filter(
                models.Q(sender=instance) | 
                models.Q(receiver=instance)
            ).delete()
            
            # Delete all notifications
            Notification.objects.filter(user=instance).delete()
            
            # Delete all message histories
            MessageHistory.objects.filter(edited_by=instance).delete()
            
            print(f"Successfully cleaned up data for user {instance.username}")
    except Exception as e:
        print(f"Error during cleanup for user {instance.username}: {str(e)}")

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id:  # Only for existing messages (edits)
        try:
            old_message = Message.objects.get(id=instance.id)
            # If content has changed, create history
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_by=instance.sender
                )
                instance.edited = True
                instance.last_edited = timezone.now()
        except Message.DoesNotExist:
            pass
