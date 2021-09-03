from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', homepage, name="home"),
    path('accounts/login/', login_attempt, name="login_attempt"),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('register/', regiser_attempt, name="register_attempt"),
    path('token/', token_send, name="token_send"),
    path('success/', success, name="success"),
    path('verify/<auth_token>', verification, name="verify"),
    path('error/', error_page, name="error"),
]