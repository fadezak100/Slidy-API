from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.validators import UniqueValidator
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField()

    def get_default_avatar():
        return settings.DEFAULT_AVATAR
    

    avatar = models.URLField(default=get_default_avatar)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)