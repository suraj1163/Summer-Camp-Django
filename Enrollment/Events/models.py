from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " - " + str(self.date) + " - " + self.location


class EventRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField()
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} registered for {self.event.name} on {self.registration_date}"