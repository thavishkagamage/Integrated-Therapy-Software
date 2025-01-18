from django.urls import path
from .views import RegisterView, UserIdView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokenrefresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserIdView.as_view(), name='user-id'),
]
