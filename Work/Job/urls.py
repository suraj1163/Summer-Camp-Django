#i want to create the all urls they can connect to the views and models and properly work in admin

from django.urls import path
from . import views

urlpatterns = [
    path("job_list/", views.job_list_api, name='job_list_api'),
    path("job_category/", views.job_category_api, name='job_category_api'),
    path("job_create/", views.job_create_api, name='job_create_api'),
]