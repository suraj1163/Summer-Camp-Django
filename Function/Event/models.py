from django.db import models

# Create your models here.

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()

    def __str__(self):
        return self.event_name


class EventRegistration_list(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_date = models.DateField()

    def __str__(self):
        return self.event.event_name
