# urls.py
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/token/', obtain_auth_token, name='obtain-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Добавьте остальные URL-шаблоны вашего приложения
]
