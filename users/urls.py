from django.urls import path
from .auth import login, register, profile

urlpatterns = [
    path('profile/',profile.ProfileView),
    path('login/',login.LoginView),
    path('register/',register.RegisterView),
]