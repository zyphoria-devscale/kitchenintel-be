from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Conversation
from .serializers import ConversationSerializer


class ConversationListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating chat conversations.
    
    GET: Returns a list of all conversations, can be filtered by session_id and role.
    POST: Creates a new conversation.
    
    This view does not require authentication.
    """
    permission_classes = [AllowAny]
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    pagination_class = None
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Optionally restricts the returned conversations to a given session_id,
        by filtering against a `session_id` query parameter in the URL.
        """
        queryset = super().get_queryset()
        session_id = self.request.query_params.get('session_id')
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        return queryset


class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific conversation.
    
    GET: Returns a single conversation by ID.
    PUT/PATCH: Updates an existing conversation.
    DELETE: Deletes a conversation.
    
    This view does not require authentication.
    """
    permission_classes = [AllowAny]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class ConversationBySessionView(APIView):
    """
    API endpoint for retrieving conversations by session_id.
    
    GET: Returns all conversations for a specific session_id.
    
    This view does not require authentication.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        """
        Returns all conversations for a specific session_id.
        Requires a session_id query parameter.
        """
        session_id = request.query_params.get('session_id')
        if not session_id:
            return Response(
                {'error': 'session_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = Conversation.objects.filter(session_id=session_id).order_by('-created_at')
        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)
