"""
URL configuration for the CBT Chatbot application.
This module defines the URL patterns for the chatbot application, including
the admin interface and the API endpoint for chatbot responses.
Routes:
- 'admin/': Admin interface provided by Django.
- 'api/chatbot/': Endpoint for chatbot responses, handled by the `chatbot_response` view.
Imports:
- admin: Django's admin module for administrative interface.
- path: Function to define URL patterns.
- chatbot_response: View function to handle chatbot API requests.
"""
from django.contrib import admin
from django.urls import path, include
from backend_function_calls.views import chatbot_response
from backend_function_calls.session_utils import get_agenda_items

from rest_framework.routers import DefaultRouter
from conversation_handler.views import ConversationViewSet, ClearConversationsView
from message_handler.views import MessageViewSet
from goal_tracking.views import GoalViewSet  # Import the GoalViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'goals', GoalViewSet, basename='goal')  # Register the goal tracking route

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chatbot/', chatbot_response, name='chatbot_response'),
    path('api/get-agenda-items/', get_agenda_items, name='get_agenda_items'),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
    path('clear_conversations/', ClearConversationsView.as_view(), name='clear-conversations'),
    path("api/", include("goal_tracking.urls")),  # Adjust based on your actual API prefix
]