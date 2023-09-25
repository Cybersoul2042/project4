import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Tweet


def index(request):
    # tweets = Tweets.objects.all()
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# For Api Routes
@csrf_exempt
@login_required
def Post(request):
    if(request.method != "POST"):
        return JsonResponse({"error" : "POST request required."}, status=400)
    
    else:
        data = json.loads(request.body)

        post = data.get("post", "")
        users = set()
        users.add(request.user)
        for user in users:
            tweet = Tweet(
                user = user,
                sender = request.user,
                senderEmail = request.user,
                post = post,
                likes = 0,
                isLiked = user == request.user
            )
            tweet.save()
        return JsonResponse({"message": "Email sent successfully."}, status=201)


def tweets(request, tweet_id):
    try:
        tweet = Tweet.objects.get(pk=tweet_id)
    except Tweet.DoesNotExist:
        return JsonResponse({'error' : 'Tweet not found'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(tweet.serialize())
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        tweet.likes = data['likes']
        tweet.isLiked = data['isLiked']
        tweet.save()
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({'error' : 'request must be either GET or PUT'}, status=400)


def tweetsType(request, tweet_view):
    if tweet_view == "myposts":
        tweets = Tweet.objects.filter(user= request.user, sender= request.user)
    elif tweet_view == "allposts":
        tweets = Tweet.objects.all()
    elif tweet_view == "otherposts":
        tweets = Tweet.objects.filter(user= request.user)
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)
    
    tweets = tweets.order_by("-tweetDate").all()
    return JsonResponse([tweet.serialize() for tweet in tweets], safe=False)
