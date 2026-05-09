from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + " - " + self.email