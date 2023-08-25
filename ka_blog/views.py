from django.shortcuts import render, redirect
from blog.models import Blog, Topic, Comment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Count


def home(request):
    topics = Topic.objects.annotate(blogcount=Count("blog"))
    blogtotalcount = Blog.objects.all().count()
    latest_posts = Blog.objects.all()[:5]  # limit number of records

    context = {
        "blogs": latest_posts,
        "topics": topics,
        "blogtotalcount": blogtotalcount,
    }  # for sidebar display
    return render(request, "latest.html", context)


def registerUser(request):
    if request.user.is_authenticated:
        return redirect("page_home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)  # automatically login user after registration
            return redirect("page_home")
        else:
            messages.error(
                request,
                "An error occured during registration. Please contact your system administrator",
            )

    form = UserCreationForm()
    context = {"form": form}
    return render(request, "login_register.html", context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("page_home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("page_home")
            else:
                messages.error(request, "The username or password does not exist!")
        except:
            messages.error(request, "User does not exist!")

    page = "login"
    context = {"page": page}
    return render(request, "login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("page_home")


def userProfile(request, pk):
    author = User.objects.get(id=pk)
    # blogtotalcount = Blog.objects.all().count()
    topics = Topic.objects.annotate(blogcount=Count("blog"))
    recent_activity = author.comment_set.all()
    blogs = author.blog_set.all()
    context = {
        "author": author,
        "topics": topics,
        # "blogtotalcount": blogtotalcount,
        "recent_activity": recent_activity,
        "blogs": blogs,
    }
    return render(request, "userprofile.html", context)
