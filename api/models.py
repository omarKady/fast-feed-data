from django.db import models
from users.models import CustomUser
# Create your models here.

class Feed(models.Model):
    feed_url = models.URLField(max_length=400)

class Content(models.Model):
    title = models.CharField(max_length=300, unique=True)
    url = models.URLField(max_length=400)
    owener = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_url(self):
        return self.url
