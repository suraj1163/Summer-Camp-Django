from django.contrib import admin
from .models import job_category
from .models import job_create
from .models import job_list

# Register your models here.
admin.site.register(job_category)
admin.site.register(job_create)
admin.site.register(job_list)