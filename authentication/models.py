from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        email = self.normalize_email(email)
        
        new_user = self.model(email, **extra_fields)

        new_user.set_password(password)

        new_user.save()

        return new_user

    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(('Superuser must have is_active=True.'))

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    username = models.CharField(max_length=25, unique=False, blank=True, null=True)
    email = models.EmailField(max_length=80, unique=True)
    phonenumber = PhoneNumberField(null=False, unique=True)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'phonenumber']

    def __str__(self):
        return f"<User {self.email}"
    
