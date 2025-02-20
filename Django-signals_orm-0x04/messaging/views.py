from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
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
        # Get the original message
        message = Message.objects.get(id=message_id)
        
        # Get all messages in the thread using MPTT
        thread_messages = Message.objects.filter(
            Q(tree_id=message.tree_id)  # Get all messages in the same tree
        ).select_related(
            'sender', 
            'receiver'
        ).prefetch_related(
            'history'
        ).order_by('tree_id', 'lft')  # Order by tree structure
        
        # Convert to threaded format
        messages = [{
            'id': msg.id,
            'content': msg.content,
            'sender': msg.sender.username,
            'receiver': msg.receiver.username,
            'timestamp': msg.timestamp,
            'level': msg.level,  # MPTT level for indentation
            'is_reply': msg.parent_message_id is not None,
            'parent_id': msg.parent_message_id
        } for msg in thread_messages]
        
        return JsonResponse({
            'messages': messages,
            'total_replies': len(messages) - 1  # Excluding original message
        })
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)

@login_required
def get_message_replies(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        
        # Get all replies using MPTT's get_descendants
        replies = Message.objects.filter(
            id__in=message.get_descendants(include_self=False)
        ).select_related(
            'sender', 
            'receiver'
        ).prefetch_related(
            'history'
        ).order_by('tree_id', 'lft')
        
        reply_data = [{
            'id': reply.id,
            'content': reply.content,
            'sender': reply.sender.username,
            'receiver': reply.receiver.username,
            'timestamp': reply.timestamp,
            'level': reply.level,
            'parent_id': reply.parent_message_id
        } for reply in replies]
        
        return JsonResponse({
            'replies': reply_data,
            'count': len(reply_data)
        })
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)
