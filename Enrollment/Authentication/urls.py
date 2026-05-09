from django.urls import path, include
from . import views

urlpatterns = [

    path('login/', views.login, name='login'),
    path('registration/', views.user_registration, name='user_registration'),
    path('user_info/', views.get_user_info, name='user_info'),
]
