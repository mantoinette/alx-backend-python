from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def chat_list(request):
    chats = [
        {"id": 1, "message": "Hello!"},
        {"id": 2, "message": "How are you?"},
    ]
    return JsonResponse(chats, safe=False)
