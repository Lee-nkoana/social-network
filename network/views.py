from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

from .models import User, Posts, Follow, Like


def index(request):
    # filter posts to show most recently posted first
    allpost = Posts.objects.all().order_by('-timeStamp')

    #Adding paginator, 10 posts per page
    paginator = Paginator(allpost, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_likes = Like.objects.all()

    posts_Liked = []
    try:
        for like in all_likes:
            if like.likedBy.id == request.user.id:
                posts_Liked.append(like.post_Liked.id)
    except:
        posts_Liked = []

    return render(request, "network/index.html", {
        "posts" : allpost,
        "page_obj" : page_obj,
        "posts_Liked" : posts_Liked
    })


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


# signed in users are able to make a new post
@login_required
def new_Post(request):
    if request.method == "GET":
        return render(request, "network/new_Post.html")
    else:
        if request.method == 'POST':
            author = request.user
            message = request.POST.get('message')

            newPost = Posts(
                author = author,
                message = message
            )

            newPost.save()

        return HttpResponseRedirect(reverse("index"))

#like post function
def add_like(request, post_id):
    post = Posts.objects.get(pk=post_id)
    post_liker = User.objects.get(pk=request.user.id)

    newLike = Like(
        post_Liked=post, 
        likedBy=post_liker
    )

    newLike.save()
    return JsonResponse({"message" : "Post has been liked"})
    

#remove like function
def remove_like(request, post_id):
    post = Posts.objects.get(pk=post_id)
    post_liker = User.objects.get(pk=request.user.id)

    unLike = Like.objects.filter(
        post_Liked=post, 
        likedBy=post_liker
    )

    unLike.delete()
    return JsonResponse({"message" : "Post has been unliked"})

#user that is logged in profile page
def profile(request, pk):
    if request.user.is_authenticated:

        #getting the user information
        profile = User.objects.get(id=pk)

        #creating the variables for the followers and following list of the user
        followers = Follow.objects.filter(user=profile) 
        following = Follow.objects.filter(followedBy=profile)


        try:
            checkFollowing = followers.filter(user=User.objects.get(pk=request.user.id))
            if len(checkFollowing) != 0:
                isFollowing = True
            else:
                isFollowing = False

        except:
            isFollowing = False


        #filtering the posts, displaying this users posts only
        userPosts = Posts.objects.filter(author=profile).order_by('-timeStamp')
        return render(request, "network/profile.html", {
            "profile" : profile,
            "userPosts" : userPosts,
            "following" : following,
            "followers" : followers,
            "isFollowing" : isFollowing
        })
    else:
        return HttpResponseRedirect(reverse("login"))

#admin: main // password:1234 

def follow_user(request):
    followUser = request.POST.get('followUser')
    followedBy = User.objects.get(pk=request.user.id)
    followerData = User.objects.get(username=followUser)

    newFollower =  Follow(
        user = followerData,
        followedBy = followedBy
    )

    newFollower.save()

    pk = followerData.id

    return HttpResponseRedirect(reverse("profile", kwargs={
        'pk' : pk
        }))

def unFollow_user(request):
    unfollowUser = request.POST.get('unfollowUser')
    unfollowedBy = User.objects.get(pk=request.user.id)
    unfollowerData = User.objects.get(username=unfollowUser)

    newUnFollow = Follow.objects.get(
        user = unfollowerData,
        followedBy = unfollowedBy
    )

    newUnFollow.delete()

    pk = unfollowerData.id

    return HttpResponseRedirect(reverse("profile", kwargs={
        'pk' : pk
        }))

def following(request):
    profile =  User.objects.get(pk=request.user.id)
    
    user_following = Follow.objects.filter(followedBy=profile)

    #filter posts to show only post from logged in users following list
    # filter posts to show most recently posted first
    allpost = Posts.objects.all().order_by('-timeStamp')

    followed_posts = []

    for post in allpost:
        for person in user_following:
            if person.user == post.author:
                followed_posts.append(post)
    
    #Adding paginator, 10 posts per page
    paginator = Paginator(followed_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj" : page_obj
    })

#function for editing a post that belongs to the user
def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Posts.objects.get(pk=post_id)
        edit_post.message = data["content"]
        edit_post.save()
        return JsonResponse({
        "message" : "Changes were successful",
        "data" : data["content"]
        })
    
