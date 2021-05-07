from django.db import models

# Create your models here.
class Post(models.Model):
    class Content():
        images = models.ImageField()
        videos = models.FileField()
        text = models.TextField()
    content = Content()
