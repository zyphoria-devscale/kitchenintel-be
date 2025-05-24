from rest_framework import serializers
from .models import Conversation


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'session_id', 'message', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']
