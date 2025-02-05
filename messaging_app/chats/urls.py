from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  # Correct import
from .views import ConversationViewSet, MessageViewSet

# Create an instance of DefaultRouter
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create a NestedDefaultRouter for messages related to conversations
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-message')

# Combine the main and nested router URLs
urlpatterns = router.urls + conversation_router.urls

