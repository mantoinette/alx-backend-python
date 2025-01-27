from django.urls import path, include
from rest_framework.routers import DefaultRouter  # Correct import
from .views import ConversationViewSet, MessageViewSet

# Initialize the DefaultRouter and register viewsets
router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

# Set up the urlpatterns
urlpatterns = [
    path("", include(router.urls)),  # Include the router URLs
]
