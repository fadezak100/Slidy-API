from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.validators import UniqueValidator

class User(AbstractUser):
    email = models.EmailField()
    avatar = models.URLField(default='http://seekpng.com/png/full/110-1100707_person-avatar-placeholder.png')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

