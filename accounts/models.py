from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length=14, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)