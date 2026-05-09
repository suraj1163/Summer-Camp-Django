from django.contrib import admin
from .models import user_application, user_application_list

# Register your models here.

admin.site.register(user_application)
admin.site.register(user_application_list)
