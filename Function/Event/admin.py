from django.contrib import admin
from Event.models import Event
from Event.models import EventRegistration_list

admin.site.register(Event)
admin.site.register(EventRegistration_list)