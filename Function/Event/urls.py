from django.urls import path,include
from Event import views

urlpatterns = [
   path("Event_list", views.Event_list, name="Event_list"),
   path("EventRegistration_list", views.EventRegistration_list, name="EventRegistration_list"),
]