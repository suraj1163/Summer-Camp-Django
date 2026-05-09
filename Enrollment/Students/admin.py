from django.contrib import admin
from .models import Students
from .models import StudentsRegistration
from .models import College
# Register your models here.



admin.site.register(Students)
admin.site.register(StudentsRegistration)
admin.site.register(College)