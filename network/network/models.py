from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    pass
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    likes = models.IntegerField(default=0)  
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)


    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"

    def update_like_count(self):
        self.likes = self.liked_by.count()
        self.save()