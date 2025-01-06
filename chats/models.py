from django.db import models

# Create your models here.
class User (models.Model):
    name = models.CharField(max_length=20)
    bio = models.TextField(blank=True, null= True)
    profile_picture = models.ImageField(upload_to= 'profile_picture')
    
    def __str__(self):
        return self.name
    
        
class Conversation (models.Model):
     participants = models.ManyToManyField(User, related_name='conversations')
     def __str__(self):
        # Return a string representation of the conversation, including its ID
        # and the usernames of all participants, formatted as "Conversation {id} with {usernames}"
        return f"Conversation {self.id} with {', '.join([user.username for user in self.participants.all()])}"
     
class Message (models.Model):
    sender = models.models.ForeignKey (User, related_name=_'Message')
    Conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,related_name='message')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
          
def __str__(self):
        # Return a string representation of the message, including the sender's username
        # and the ID of the conversation it belongs to
        return f"Message from {self.sender.username} in Conversation {self.conversation.id}"