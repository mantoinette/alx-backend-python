from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.

@login_required
@require_http_methods(["DELETE"])
def delete_user(request):
    """
    View to handle user account deletion with transaction support
    """
    try:
        with transaction.atomic():  # Add transaction support
            user = request.user
            # Get counts for user feedback
            messages_count = user.sent_messages.count() + user.received_messages.count()
            history_count = MessageHistory.objects.filter(edited_by=user).count()
            
            user.delete()  # This will trigger the post_delete signal
            
            return JsonResponse({
                'message': 'User account deleted successfully',
                'deleted_data': {
                    'messages': messages_count,
                    'history_entries': history_count
                }
            }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
