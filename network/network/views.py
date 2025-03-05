from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)


    return render(request, "network/index.html", {
        'page_obj': page_obj
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

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post = Post.objects.create(user=request.user, content=content)
            return JsonResponse({'message': 'Post published!'}, status=200)
        else:
            return JsonResponse({'error': 'Post is empty!'}, status=400)
    return redirect('index')

def all_posts(request):
    posts = Post.objects.all().order_by('-created_at')

    for post in posts:
        post.user_has_liked = request.user in post.liked_by.all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/all_posts.html", {
        'page_obj': page_obj
    })

@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user_profile).order_by('-created_at')
    followers = user_profile.followers.count()
    following = user_profile.following.count()

    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/profile.html", {
        "user_profile": user_profile,
        "user": request.user,
        "page_obj": page_obj,
        "followers": followers,
        "following": following
    })

@login_required
def follow(request, username):
    follow_user = User.objects.get(username=username)

    if follow_user != request.user:
        if follow_user not in request.user.following.all():
            request.user.following.add(follow_user)
        else:
            request.user.following.remove(follow_user)
    
    return redirect('profile', username=username)

@login_required
def  following(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(user__in=following_users).order_by('-created_at')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

@login_required
def edit_post(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            post = Post.objects.get(id=post_id, user=request.user)
            post.content = data["content"]
            post.save()
            return JsonResponse({"success": True})
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.liked_by.all():
        post.liked_by.remove(user)
        liked = False
    else:
        post.liked_by.add(user)
        liked = True

    post.save()
    
    return JsonResponse({
        'success': True,
        'new_like_count': post.liked_by.count(),
        'user_has_liked': liked  
    })