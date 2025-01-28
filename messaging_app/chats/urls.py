from django.urls import path, include
from rest_framework.routers import DefaultRouter  # Ensure DefaultRouter is imported
from rest_framework_nested.routers import NestedDefaultRouter  # Ensure NestedDefaultRouter is imported
from .views import ConversationViewSet, MessageViewSet  # Ensure the views are correctly imported

# Main router for conversations
router = DefaultRouter()  # Create an instance of DefaultRouter
router.register(r'conversations', ConversationViewSet, basename='conversation')  # Register the ConversationViewSet

# Nested router for messages related to conversations
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')  # Create a NestedDefaultRouter
conversation_router.register(r'messages', MessageViewSet, basename='conversation-message')  # Register the MessageViewSet

# Combine the main and nested router URLs
urlpatterns = [
    path('', include(router.urls)),              # Include the main router
    path('', include(conversation_router.urls)),  # Include the nested router
]
