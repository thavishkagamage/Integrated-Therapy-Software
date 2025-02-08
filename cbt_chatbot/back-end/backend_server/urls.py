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
from conversation_handler.views import ConversationViewSet, ClearConversationsView
from message_handler.views import MessageViewSet

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chatbot/', chatbot_response, name='chatbot_response'),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
    path('clear_conversations/', ClearConversationsView.as_view(), name='clear-conversations'),

    # Wagtail

    # wagtailadmin_urls provides the admin interface for Wagtail. 
    # This is separate from the Django admin interface, django.contrib.admin. 
    path('cms/', include(wagtailadmin_urls)),

    # Wagtail serves your document files from the location, wagtaildocs_urls. 
    # You can omit this if you do not intend to use Wagtail’s document management features.
    path('documents/', include(wagtaildocs_urls)),

    # Wagtail serves your pages from the wagtail_urls location. In the above example, Wagtail handles URLs under /pages/, 
    # leaving your Django project to handle the root URL and other paths as normal
    path('pages/', include(wagtail_urls)),

    # If you want Wagtail to handle the entire URL space including the root URL, then place this at the end of the urlpatterns list.
    # path('', include(wagtail_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Note:
# This only works in development mode (DEBUG = True); in production, you have to configure your web server to serve files from MEDIA_ROOT. 