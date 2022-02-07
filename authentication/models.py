from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PreRegistration(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password1 = models.CharField(max_length=40)
    password2 = models.CharField(max_length=40)
    otp = models.CharField(max_length=10, default='DEFAULT VALUE')

