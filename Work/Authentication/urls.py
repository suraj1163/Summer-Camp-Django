from django.urls import path
from . import views

urlpatterns = [
    path('user_register/', views.user_register_api, name='user_register_api'),
    path('user_login/', views.user_login_api, name='user_login_api'),
    path('user_profile/', views.user_profile_api, name='user_profile_api')

]
