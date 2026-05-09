from django.urls import path
from .import views

urlpatterns = [
    path("", views.college, name="college"),
    path("students/", views.Students, name="students"),
    path("<int:pk>/", views.student_details, name="college"),
]