from django.contrib import admin
from .models import user_register, user_login, user_profile


# Register your models here.

admin.site.register(user_register)
admin.site.register(user_login)
admin.site.register(user_profile)
