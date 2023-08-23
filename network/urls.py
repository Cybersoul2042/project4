
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #Api Routes

    path("tweets", views.Post, name="NewTweet"),
    path("tweets/<int:tweet_id>", views.tweets, name="SentTweet"),
    path("tweets/<str:tweet_view>", views.tweetsType, name="TweetView")
]
