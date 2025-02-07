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
