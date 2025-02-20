from django.contrib import admin
from .models import Message, MessageHistory

class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    readonly_fields = ('edited_at', 'edited_by', 'old_content')
    extra = 0

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'edited', 'last_edited')
    inlines = [MessageHistoryInline]

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'edited_at', 'edited_by')
    readonly_fields = ('message', 'edited_at', 'edited_by', 'old_content')
