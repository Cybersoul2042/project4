from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.postgres.fields import ArrayField
# from django.utils import timezone


class User(AbstractUser):
    pass

class Tweet(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sender = models.ForeignKey("User", related_name="Sender_Of_The_Tweet", on_delete=models.PROTECT)
    senderEmail = models.ForeignKey("User", related_name="Sender_Email", on_delete=models.CASCADE)
    post = models.TextField(blank=True)
    likes = models.IntegerField(default=0)
    isLiked = models.BooleanField(default=False)
    tweetDate = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "senderEmail": self.senderEmail.email,
            "post": self.post,
            "likes": self.likes,
            "isLiked": self.isLiked,
            "tweetDate": self.tweetDate.strftime("%b %d %Y, %I:%M %p")
        }

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User,  blank=True, related_name="follower_users")
    followings = models.ManyToManyField(User,  blank=True, related_name="following_users")

    def __str__(self):
        return self.user.username
