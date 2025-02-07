from rest_framework import serializers
from .models import Goal

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'user', 'name', 'progress', 'completed', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
