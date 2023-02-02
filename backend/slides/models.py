from django.db import models
from django.conf import settings

from cloudinary.models import CloudinaryField

User = settings.AUTH_USER_MODEL

class Slide(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    url = CloudinaryField('slide', resource_type="auto", blank=True)
    is_public = models.BooleanField(default=True)
    is_live = models.BooleanField(default=False)
