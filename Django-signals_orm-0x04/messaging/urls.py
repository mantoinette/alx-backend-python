from django.urls import path
from . import views

urlpatterns = [
    # ... your other URL patterns ...
    path('delete-account/', views.delete_user, name='delete_user'),
]
