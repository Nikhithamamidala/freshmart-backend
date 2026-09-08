from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, default='customer')
    status = models.CharField(max_length=20, default='active')