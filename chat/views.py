from rest_framework import generics

from .models import Conversation
from .serializers import ConversationSerializer


class ConversationListCreateView(generics.ListAPIView):
    """
    API endpoint for listing and creating chat conversations.
    
    GET: Returns a list of all conversations, can be filtered by session_id.
    POST: Creates a new conversation.
    """
    serializer_class = ConversationSerializer
    pagination_class = None
    
    def get_queryset(self):
        """
        Optionally restricts the returned conversations to a given session_id,
        by filtering against a `session_id` query parameter in the URL.
        """
        session_id = self.request.query_params.get('session_id')
        if session_id:
            queryset = Conversation.objects.filter(session_id=session_id).order_by('-created_at')
        else:
            queryset = Conversation.objects.all().order_by('-created_at')
        return queryset