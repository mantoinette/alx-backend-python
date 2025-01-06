from .models import User, Conversation, Message
from rest_framework import  serializers

class UserSerializer(serializers.ModelSerializer):
    class meta:
        model = User
        fields = '__all__'
        
class ConversationSerializer(serializers.ModelSerializer):
    class meta:
        model = Conversation
        fields = '__all__'
        
class Message (serializers.ModelSerializer):
    class meta:
        model = Message
        field = '__all__'
        