from django.db import models
from Job.models import job_create
from Authentication.models import user_register 

class user_application(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.IntegerField()
    resume=models.FileField(upload_to='resume/')
    job=models.ForeignKey('Job.job_create',on_delete=models.CASCADE)
    user=models.ForeignKey('Authentication.user_register',on_delete=models.CASCADE)
    
class user_application_list(models.Model):
    application=models.ForeignKey('user_application',on_delete=models.CASCADE)
    job=models.ForeignKey('Job.job_create',on_delete=models.CASCADE)
    user=models.ForeignKey('Authentication.user_register',on_delete=models.CASCADE)

