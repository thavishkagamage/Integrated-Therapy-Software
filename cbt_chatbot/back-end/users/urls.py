from django.urls import path
from .views import RegisterView, UserIdView, MyTokenObtainPairView, UserInfoView, DeleteUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokenrefresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserIdView.as_view(), name='user-id'),
    path('userinfo/', UserInfoView.as_view(), name='user-info'),
    path('delete-profile/', DeleteUserView.as_view(), name='delete-profile'),
]
