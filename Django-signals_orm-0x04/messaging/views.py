from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Message

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

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver_id = request.POST.get('receiver')
        parent_id = request.POST.get('parent_message')  # For replies
        
        message = Message.objects.create(
            sender=request.user,
            receiver_id=receiver_id,
            content=content,
            parent_message_id=parent_id
        )
        return JsonResponse({'status': 'success'})

@login_required
def get_thread(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        thread = (
            Message.objects
            .filter(tree_id=message.tree_id)
            .select_related('sender', 'receiver')  # Optimize queries
            .prefetch_related('history')  # Optimize queries
            .order_by('tree_id', 'lft')
        )
        
        # Convert queryset to list of dictionaries for JSON response
        messages = [{
            'id': msg.id,
            'content': msg.content,
            'sender': msg.sender.username,
            'receiver': msg.receiver.username,
            'timestamp': msg.timestamp,
            'is_reply': msg.parent_message_id is not None
        } for msg in thread]
        
        return JsonResponse({'messages': messages})
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)
