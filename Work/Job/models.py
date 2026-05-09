from django.db import models
# Create your models here.

class job_category(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class job_create(models.Model):
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.IntegerField()
    location = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(job_category,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.company_name + " - " + self.position + " - " + self.location + " - " + str(self.salary)

class job_list(models.Model):
    category = models.ForeignKey(job_category,on_delete=models.CASCADE)
    job = models.ForeignKey(job_create,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category.name} - {self.job}"