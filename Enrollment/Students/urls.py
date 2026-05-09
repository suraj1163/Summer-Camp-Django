from django.urls import path,include
from . import views


urlpatterns = [
    path("colleges/", views.college_list_api, name="colleges"),
    path("", views.student_list_api, name="Students"),
    path("Students/", views.student_list_api, name="Students"),
    path("StudentsRegistration/", views.StudentsRegistrations, name="StudentsRegistration"),
    path('<int:college_id>/',views.student_detail,name='student_detail'),
    path('auth/',include('Authentication.urls'))
]