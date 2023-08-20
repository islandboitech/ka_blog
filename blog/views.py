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
    topics = Topic.objects.annotate(blogcount=Count("blog"))
    context = {"blogs": blogs, "topics": topics, "blogtotalcount": blogtotalcount}
    return render(request, "blog/blogs.html", context)


def blog(request, pk):
    blog = Blog.objects.get(id=pk)

    if request.method == "POST":
        comment = Comment.objects.create(
            user=request.user, blog=blog, comment=request.POST.get("comment")
        )
        return redirect("page-blog", pk=blog.id)

    comments = blog.comment_set.all().order_by("-created")
    context = {"blog": blog, "comments": comments}
    return render(request, "blog/blog.html", context)


@login_required(login_url="login")
def new_blog(request):
    if request.method == "POST":
        form = FormBlog(request.POST)
        if form.is_valid():
            form.save()
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
