from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField()
    avatar = models.TextField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
