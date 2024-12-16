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

from rest_framework.routers import DefaultRouter
from conversation_handler.views import ConversationViewSet
from message_handler.views import MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chatbot/', chatbot_response, name='chatbot_response'),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
]