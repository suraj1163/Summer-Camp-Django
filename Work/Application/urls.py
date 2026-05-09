from django.urls import path
from . import views

urlpatterns = [
    path("user_application",views.user_application_api, name='user_application_api'),
    path("user_application_list",views.user_application_list_api, name='user_application_list_api')
]