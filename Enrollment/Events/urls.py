from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.event_list_api, name="Events"),
]