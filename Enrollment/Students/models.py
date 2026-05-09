from django.db import models
from Events.models import Event

# Create your models here.

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    College = models.CharField(max_length=100)
    def __str__(self):
        return self.name + " - " + str(self.age) + " - " + self.email + " - " + self.College

class StudentsRegistration(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    event = models.ForeignKey('Events.Event', on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.student.name} registered for {self.event.name} on {self.registration_date}"
    

class College(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name+ " - " + self.address + " - " + self.phone + " - "  