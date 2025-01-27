from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Use DefaultRouter to register viewsets
router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

# Include the router's URLs in the urlpatterns
urlpatterns = [
    path("", include(router.urls)),  # Register routes from the router
]
