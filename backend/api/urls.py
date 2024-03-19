from django.urls import path
from userauths import views as userauths_views
from store import views as store_views

urlpatterns = [
    path('user/token/', userauths_views.MyTokenObtainPairView.as_view())
]