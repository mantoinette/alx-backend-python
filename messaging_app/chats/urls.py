from django.urls import path, include
from rest_framework.routers import DefaultRouter  # Import DefaultRouter
from rest_framework_nested import routers  # Import Nested router
from .views import ConversationViewSet, MessageViewSet

# Create an instance of DefaultRouter
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages related to conversations
conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-message')

# Combine the two routers: main and nested
urlpatterns = router.urls + conversation_router.urls
