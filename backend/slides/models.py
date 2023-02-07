from django.db import models
from django.conf import settings

from cloudinary.models import CloudinaryField

User = settings.AUTH_USER_MODEL


class Slide(models.Model):
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name='slides_info')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    slide = CloudinaryField(blank=True, resource_type="auto")
    url = models.URLField(blank=True)
    is_public = models.BooleanField()
    is_live = models.BooleanField()
