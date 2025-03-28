from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50,
        choices=[('active', 'Active'), ('archived', 'Archived'), ('deleted', 'Deleted')],
        default='active'
    )
    session_number = models.IntegerField(default=0)
    agenda_items = models.JSONField(default=dict)
    current_sub_items = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.title or 'Conversation'} - {self.user.username}"