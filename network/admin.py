from django.contrib import admin
from .models import User, Tweet

# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    user_lists = ("id", "username", "email")
class UsersTweets(admin.ModelAdmin):
    tweets_list = ("id", "user", "tweetText", "tweetDate")

admin.site.register(User, UsersAdmin)
admin.site.register(Tweet, UsersTweets)