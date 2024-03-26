from django.urls import path
from userauths import views as userauths_views
from store import views as store_views

from rest_framework_simplejwt.views import TokenRefreshView

# Define URL patterns
urlpatterns = [
    # Define path for obtaining token pairs using MyTokenObtainPairView
    path("user/token/", userauths_views.MyTokenObtainPairView.as_view()),
    # Define path for refreshing access and refresh tokens using TokenRefreshView
    path("user/token/refresh/", TokenRefreshView.as_view()),
    # Define a path for user registeration using RegisterView
    path("user/register/", userauths_views.RegisterView.as_view()),
    # Define a path for user password reset using PasswordResetAPI
    path("user/password-reset/<email>/", userauths_views.PasswordResetAPI.as_view(), name='password_change'),
    
    path("user/password-change/", userauths_views.PasswordChangeApi.as_view(), name='password_change'),
    
]
