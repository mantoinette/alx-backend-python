from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["DELETE"])
def delete_user(request):
    """
    View to handle user account deletion
    """
    try:
        user = request.user
        user.delete()  # This will trigger the post_delete signal
        return JsonResponse({'message': 'User account deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal to clean up all user-related data after account deletion
    Note: Most deletions will be handled by CASCADE, this is for any additional cleanup
    """
    # The CASCADE setting on the foreign keys will automatically handle:
    # - Messages where user was sender or receiver
    # - Notifications belonging to the user
    # - MessageHistory entries where user was editor
    
    # Any additional cleanup can be added here
    pass
