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


def getActivity(pk, current_user, limit=5):
    # variable declarations
    # start: queryset UNION BLOG and COMMENT for recent activity
    qsBlog = Blog.objects.all().values('id', 'author', 'author__username', 'author__avatar', 'created', 'updated', 'isupdated', 'title').annotate(comment=Value(''), action1=Value('Posted a blog'), action2=Value('Edited a blog'))

    if current_user:
        qsBlog=qsBlog.filter(author__id__iexact=pk)

    qsComment = Comment.objects.all().values('blog__id', 'author', 'author__username', 'author__avatar', 'created', 'updated', 'isupdated', 'blog__title', 'comment').annotate(action1=Value('Wrote a comment to'), action2=Value('Edited a comment'))

    if current_user:
        qsComment=qsComment.filter(author__id__iexact=pk)
    
    recent=qsBlog.union(qsComment).order_by('-updated', '-created')

    # print(recent)
    return recent[:limit] if limit > 0 else recent
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
    context = {"form": form, 'pagetitle': 'Create an Account'}
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
                messages.success(request, f"Login seccessful. You are logged in as @{user.username}.")
                return redirect("page-blogs")
            else:
                messages.error(request, "The email or password does not exist!")
        except:
            messages.error(request, "User does not exist!")

    page = "login"
    context = {"page": page, 'pagetitle': 'Log in'}
    return render(request, "creds/login_register.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, f"You have been successfully logged out.")
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
    # activity=getActivity(pk)
    context = {
        "user": author,
        "topics": topics,
        "recent": getActivity(pk, False, 5),
        "user_activity": getActivity(pk, True, 0),
        # "blogtotalcount": blogtotalcount,
        # "recent_activity": recent_activity,
        "blogs": blogs,
        "pagetitle": 'User Profile'
    }
    print(len(context['user_activity']))
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
    context={'form':form, 'pagetitle':"Update Profile"}
    return render(request, 'creds/form_edit_userprofile.html', context)