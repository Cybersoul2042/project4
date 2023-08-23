from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Tweets(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sender = models.ForeignKey("User", related_name="Sender_Of_The_Tweet", on_delete=models.PROTECT)
    reply = models.BooleanField(default=False)
    post = models.TextField(blank=True)
    likes = models.IntegerField(default=0)
    tweetDate = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.email,
            "reply": self.reply,
            "post": self.post,
            "likes": self.likes,
            "tweetDate": self.tweetDate.strftime("%b %d %Y, %I:%M %p")
        }

class Profiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User,  blank=True, related_name="follower_users")
    followings = models.ManyToManyField(User,  blank=True, related_name="following_users")

    def __str__(self):
        return self.user.username
