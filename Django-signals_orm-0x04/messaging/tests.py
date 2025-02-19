from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

# Create your tests here.

class MessageNotificationTest(TestCase):
    def setUp(self):
        # Create test users
        self.sender = User.objects.create_user('sender', 'sender@test.com', 'password123')
        self.receiver = User.objects.create_user('receiver', 'receiver@test.com', 'password123')

    def test_notification_creation(self):
        # Create a new message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Test message"
        )

        # Check if notification was automatically created
        notification = Notification.objects.filter(
            user=self.receiver,
            message=message
        ).first()

        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

    def test_message_creation(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello!"
        )

        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.content, "Hello!")
        self.assertFalse(message.is_read)
