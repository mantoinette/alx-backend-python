from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from .models import Message
from django.views.decorators.cache import cache_page

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
@cache_page(60)  # Cache the view for 60 seconds
def conversation_messages(request, conversation_id):
    """Display messages in a conversation with caching"""
    messages = (
        Message.objects
        .filter(conversation_id=conversation_id)
        .select_related('sender')
        .order_by('timestamp')
    )
    
    messages_data = [{
        'id': msg.id,
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp.isoformat(),
        'is_read': msg.is_read
    } for msg in messages]
    
    return JsonResponse({
        'conversation_id': conversation_id,
        'messages': messages_data
    })

@login_required
def send_message(request, conversation_id):
    """Send a new message (not cached)"""
    if request.method == 'POST':
        content = request.POST.get('content')
        message = Message.objects.create(
            conversation_id=conversation_id,
            sender=request.user,
            content=content
        )
        return JsonResponse({
            'status': 'success',
            'message_id': message.id
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

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

@login_required
def inbox(request):
    """Display user's unread messages"""
    # Use unread manager and optimize with .only()
    unread_messages = Message.unread.unread_for_user(request.user).only(
        'id',
        'sender__username',
        'content',
        'timestamp',
        'is_read'
    )
    
    messages_data = [{
        'id': msg.id,
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp
    } for msg in unread_messages]
    
    return JsonResponse({'unread_messages': messages_data})

@login_required
def mark_messages_read(request):
    """Mark multiple messages as read"""
    if request.method == 'POST':
        message_ids = request.POST.getlist('message_ids')
        Message.unread.mark_as_read(message_ids, request.user)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_unread_count(request):
    """Get count of unread messages"""
    count = Message.unread.unread_for_user(request.user).only('id').count()
    return JsonResponse({'unread_count': count})
