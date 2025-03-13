from django.test import TestCase
from django.contrib.auth.models import User
from .models import Goal

class GoalModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.goal = Goal.objects.create(user=self.user, name='Test Goal', progress=50)

    def test_goal_creation(self):
        self.assertEqual(self.goal.name, 'Test Goal')
        self.assertEqual(self.goal.progress, 50)
        self.assertFalse(self.goal.completed)

    def test_goal_update(self):
        self.goal.progress = 75
        self.goal.save()
        self.assertEqual(self.goal.progress, 75)

    def test_goal_deletion(self):
        goal_id = self.goal.id
        self.goal.delete()
        self.assertFalse(Goal.objects.filter(id=goal_id).exists())
