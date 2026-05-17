from django.contrib import admin
from jobs.models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'posted_by', 'created_at')
    list_filter = ('company', 'created_at')
    search_fields = ('title', 'company', 'description')
