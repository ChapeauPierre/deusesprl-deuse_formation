import user.api_views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path


app_name = 'api_user'
urlpatterns = [
    # Token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/current/', user.api_views.UserCurrentView.as_view(), name='user_current'),
]
