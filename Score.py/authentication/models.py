from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=[('scorer', 'Scorer'), ('viewer', 'Viewer')], default='scorer')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
