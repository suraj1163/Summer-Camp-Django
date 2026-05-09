from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class user_register_manager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class user_register(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = user_register_manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.name + " - " + self.email

    @property
    def is_staff(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class user_login(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.email + " - " + self.password

class user_profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    city = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name + " - " + self.email + " - " + str(self.phone) + " - " + self.city + " - " + str(self.date)

    
    
    