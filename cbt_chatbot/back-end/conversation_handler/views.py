from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Conversation
from .serializers import ConversationSerializer
from rest_framework import viewsets

class ClearConversationsView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        conversations = Conversation.objects.filter(user=user)
        conversations.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(user=user)