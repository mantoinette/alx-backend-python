from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("chats.urls")),  # Make sure this line is added to include the chats app's URLs
    path('api-auth/', include('rest_framework.urls')),  # Add this line
]
