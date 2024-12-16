from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'created_at', 'metadata']

    def create(self, validated_data):
        # Create a new Message instance with the validated data
        message = Message.objects.create(**validated_data)
        return message