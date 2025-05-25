from django.urls import path
from .views import ConversationListCreateView

urlpatterns = [
    path('chats/', ConversationListCreateView.as_view(), name='conversation-list'),
]
