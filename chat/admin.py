from django.contrib import admin
from .models import Conversation


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_id', 'message', 'role', 'created_at')
    list_filter = ('session_id', 'role')
    search_fields = ('session_id', 'message', 'role')
    ordering = ('-created_at',)

admin.site.register(Conversation, ConversationAdmin)
