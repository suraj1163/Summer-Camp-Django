from django.db import models
from Dashboard.models import Students


# Create your models here.
class college(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name + " - " + self.address + " - " + self.phone
    
class StudentRegistration(models.Model):
    college = models.ForeignKey(college, on_delete=models.CASCADE)
    student = models.ForeignKey(Students, on_delete=models.CASCADE) 
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.college} - {'Registered' if self.is_registered else 'Not Registered'}"
    
