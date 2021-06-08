from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    #publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()
    images = models.ImageField()
    videos = models.ImageField()
    text = models.TextField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Comment, self).save(*args, **kwargs)
