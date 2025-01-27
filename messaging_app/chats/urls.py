from django.urls import path, include  # Make sure to import path and include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers  # Nested router for nested URLs
from .views import ConversationViewSet, MessageViewSet

# Initialize the default router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create the nested router for messages related to conversations
conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-message')

# Combine the main router and the nested router
urlpatterns = router.urls + conversation_router.urls
