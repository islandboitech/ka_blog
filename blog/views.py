from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Blog, Topic, Comment
from .forms import FormBlog
from django.db.models import Count, Q


# Create your views here.
def blogs(request):
    # topics = Topic.objects.all()
    q = request.GET.get("q") if request.GET.get("q") != None else ""  # search criteria
    blogtotalcount = Blog.objects.all().count()
    # blogs = Blog.objects.filter(topic__name__icontains=q)
    blogs = Blog.objects.filter(
        Q(topic__name__icontains=q)
        | Q(title__icontains=q)
        | Q(description__icontains=q)
        | Q(author__username__icontains=q)
    )
    # recent_activity = Comment.objects.all()[:5] # show all messages regardless of topic
    recent_activity = Comment.objects.filter(Q(blog__topic__name__icontains=q))[
        :5
    ]  # show messages based on the topic selected
    topics = Topic.objects.annotate(blogcount=Count("blog"))
    context = {
        "blogs": blogs,
        "topics": topics,
        "blogtotalcount": blogtotalcount,
        "recent_activity": recent_activity,
    }
    return render(request, "blog/blogs.html", context)


def blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.method == "POST":
        comment = Comment.objects.create(
            author=request.user, blog=blog, comment=request.POST.get("comment")
        )
        blog.participants.add(request.user)
        return redirect("page-blog", pk=blog.id)

    blogtotalcount = Blog.objects.all().count()
    topics = Topic.objects.annotate(blogcount=Count("blog"))
    participants = blog.participants.all()
    # comments = blog.comment_set.all().order_by("-created")
    comments = blog.comment_set.all()  # ordering is defined in the model directly
    context = {
        "blog": blog,
        "comments": comments,
        "participants": participants,
        "topics": topics,
        "blogtotalcount": blogtotalcount,
    }
    return render(request, "blog/blog.html", context)


@login_required(login_url="login")
def new_blog(request):
    if request.method == "POST":
        form = FormBlog(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("page_home")
    else:
        form = FormBlog()
        context = {"pagetitle": "Add New Blog", "form": form}
        return render(request, "blog/form_blog.html", context)


@login_required(login_url="login")
def update_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.user != blog.author:
        return HttpResponse(
            "You are not allowed to edit or delete a blog created by others."
        )

    if request.method == "POST":
        form = FormBlog(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("page_home")
    else:
        form = FormBlog(instance=blog)
        context = {"pagetitle": "Update Blog", "form": form}
        return render(request, "blog/form_blog.html", context)


@login_required(login_url="login")
def delete_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.user != blog.author:
        return HttpResponse(
            "You are not allowed to edit or delete a blog created by others."
        )
    blog.delete()
    return redirect("page_home")


@login_required(login_url="login")
def delete_comment(request, blogid, pk):
    comment = Comment.objects.get(id=pk)
    if request.user != comment.author:
        return HttpResponse(
            "You are not allowed to edit or delete a comment created by others."
        )
    comment.delete()
    return redirect("page-blog", pk=blogid)
