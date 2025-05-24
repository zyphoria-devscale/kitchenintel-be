from django.urls import path
from .views import ConversationListCreateView, ConversationDetailView, ConversationBySessionView

urlpatterns = [
    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list'),
    path('conversations/<str:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/by-session/', ConversationBySessionView.as_view(), name='conversation-by-session'),
]
