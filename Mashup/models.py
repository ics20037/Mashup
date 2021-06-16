from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "posts")

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "comments")
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.TextField()
    friends = models.ManyToManyField(User, related_name = "friends")

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_posts(self):
        return self.user.posts.all()

    def get_feed_posts(self):
        posts = []

        for friend in self.get_friends():
            for post in friend.profile.get_posts():
                posts.append(post)

        for post in self.get_posts():
            posts.append(post)

        return posts

    def get_friends(self):
        return self.friends.all()

    def add_friend(self, user):
        self.friends.add(user)
        user.profile.friends.add(self.user)

    def is_friend(self, user):
        if user in self.friends.all():
            return True
        return False

    def remove_friend(self, user):
        if user in self.friends.all():
            self.friends.remove(user)
            user.profile.friends.remove(self.user)
