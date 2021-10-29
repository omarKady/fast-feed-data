from django.db import models
from users.models import CustomUser
# Create your models here.

class Feed(models.Model):
    title = models.CharField(max_length=300, unique=True)
    url = models.URLField(max_length=400)
    feed_link = models.CharField(max_length=400, default="", blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_url(self):
        return self.url
