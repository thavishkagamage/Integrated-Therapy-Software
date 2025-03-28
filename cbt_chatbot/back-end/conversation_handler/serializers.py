from rest_framework import serializers
from .models import Conversation
from message_handler.serializers import MessageSerializer

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'title', 'status', 'messages', 'created_at', 'updated_at', 'session_number', 'agenda_items', 'current_sub_items']

    def create(self, validated_data):
        user = validated_data.pop('user')
        conversation = Conversation.objects.create(user=user, **validated_data)
        return conversation