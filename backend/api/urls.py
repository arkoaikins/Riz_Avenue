from django.urls import path
from userauths import views as userauths_views
from store import views as store_views

# Define URL patterns
urlpatterns = [
    # Define path for obtaining token pairs using MyTokenObtainPairView
    path("user/token/", userauths_views.MyTokenObtainPairView.as_view()),
    # Define a path for user registeration using RegisterView
    path("user/register/", userauths_views.RegisterView.as_view()),
]
