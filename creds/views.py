from django.shortcuts import render, redirect
from blog.models import Blog, Topic, Comment
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import userRegistrationForm
from django.db.models import Count, Q, Value
from django.contrib.auth.decorators import login_required
from .forms import FormUserProfile, userRegistrationForm
# from django.contrib.auth.models import User
from .models import User


def getRecentActivity(pk):
    # variable declarations
    # start: queryset UNION BLOG and COMMENT for recent activity
    qsBlog = Blog.objects.all().values('id', 'author', 'author__username', 'author__avatar', 'created', 'updated', 'isupdated', 'title').annotate(comment=Value(''), action1=Value('Posted a blog'), action2=Value('Edited a blog')).filter(author__id__iexact=pk)
    qsComment = Comment.objects.all().values('id', 'author', 'author__username', 'author__avatar', 'created', 'updated', 'isupdated', 'blog__title', 'comment').annotate(action1=Value('Wrote a comment to'), action2=Value('Edited a comment')).filter(author__id__iexact=pk)
    recent=qsBlog.union(qsComment).order_by('-updated', '-created')[:5]
    # print(recent)
    return recent
    # end: queryset UNION

def registerUser(request):
    if request.user.is_authenticated:
        return redirect("page-blogs")

    if request.method == "POST":
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)  # automatically login user after registration
            messages.success(request, f"Registration successful. You are now logged in as @{user.username}." )
            return redirect("page-blogs")
        else:
            messages.error(
                request,
                "Unsuccessful registration. Invalid information.",
            )

    form = userRegistrationForm()
    context = {"form": form}
    return render(request, "creds/login_register.html", context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("page-blogs")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            # print(user)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.error(request, f"Login seccessful. You are logged in as @{user.username}.")
                return redirect("page-blogs")
            else:
                messages.error(request, "The email or password does not exist!")
        except:
            messages.error(request, "User does not exist!")

    page = "login"
    context = {"page": page}
    return render(request, "creds/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("page-blogs")


def userProfile(request, pk):
    author = User.objects.get(id=pk)
    blogs = author.blog_set.all().annotate(countcomments=Count("comment"))
    # blogtotalcount = Blog.objects.all().count()
    topics = Topic.objects.annotate(blogcount=Count(
        "blog",
        Q(blog__author__id__iexact=pk)
        ))
    # recent_activity = author.comment_set.all()
    recent=getRecentActivity(pk)
    context = {
        "user": author,
        "topics": topics,
        "recent": recent,
        # "blogtotalcount": blogtotalcount,
        # "recent_activity": recent_activity,
        "blogs": blogs,
    }
    return render(request, "creds/userprofile.html", context)


@login_required(login_url='login')
def edit_userprofile(request):
    user=request.user
    if request.method=='POST':
        form=FormUserProfile(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    form=FormUserProfile(instance=user)
    context={'form':form, 'pagetitle':"Edit Profile"}
    return render(request, 'creds/form_edit_userprofile.html', context)