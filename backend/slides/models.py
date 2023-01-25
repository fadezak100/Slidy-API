from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Slide(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    url = models.URLField()
    public = models.BooleanField(default=True)
    live = models.BooleanField(default=False)

    def is_public(self):
        return self.private
    
    def is_live(self):
        return self.live
