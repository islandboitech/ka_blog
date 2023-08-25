from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Blog, Topic, Comment
from .forms import FormBlog, FormUserProfile
from django.db.models import Count, Q
from django.contrib import messages
# {{request.META.HTTP_REFERER}} # use this link to go back to the previous page (used in delete form in this system)

# Create your views here.
def blogs(request):
    # topics = Topic.objects.all()
    q = request.GET.get("q") if request.GET.get("q") != None else ""  # search criteria
    # blogs = Blog.objects.filter(topic__name__icontains=q)
    blogs = Blog.objects.filter(
        Q(topic__name__icontains=q)
        | Q(title__icontains=q)
        | Q(description__icontains=q)
        | Q(author__username__icontains=q)
    )
    # recent_activity = Comment.objects.all()[:5] # show all messages regardless of topic
    recent_activity = Comment.objects.filter(Q(blog__topic__name__icontains=q))[:5]  # show messages based on the topic selected
    topics = Topic.objects.annotate(blogcount=Count("blog"))
    context = {"blogs": blogs, "topics": topics, "recent_activity": recent_activity, }
    return render(request, "blog/blogs.html", context)


def blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.method == "POST":
        comment = Comment.objects.create(author=request.user, blog=blog, comment=request.POST.get("comment"))
        blog.participants.add(request.user)
        return redirect("page-blog", pk=blog.id)
    topics = Topic.objects.annotate(blogcount=Count("blog"))
    participants = blog.participants.all()
    # comments = blog.comment_set.all().order_by("-created")
    comments = blog.comment_set.all()  # ordering is defined in the model directly
    context = {
        "blog": blog,
        "comments": comments,
        "participants": participants,
        "topics": topics,
    }
    return render(request, "blog/blog.html", context)


@login_required(login_url="login")
def new_blog(request):
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        try:
            topic, created = Topic.objects.get_or_create(name=topic_name)  # get existing or create a new topic in the database
            Blog.objects.create(
                author=request.user,
                topic=topic,
                title=request.POST.get('title'),
                description=request.POST.get('description')
            )
            return redirect("page_home")
        except:
            messages.error(request, "An error occured while saving the blog.")
            return redirect("new-blog")
        # form = FormBlog(request.POST)
        # if form.is_valid():
        #     blog = form.save(commit=False)
        #     blog.author = request.user
        #     blog.save()
    else:
        topics = Topic.objects.all()
        form = FormBlog()
        context = {"pagetitle": "Add New Blog", "form": form, "topics": topics}
        return render(request, "blog/form_blog.html", context)


@login_required(login_url="login")
def update_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.user != blog.author:
        return HttpResponse("You are not allowed to edit or delete a blog created by others.")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)  # get existing or create a new topic in the database
        blog.topic=topic
        blog.title=request.POST.get('title')
        blog.description=request.POST.get('description')
        blog.save()

        # form = FormBlog(request.POST, instance=blog)
        # if form.is_valid():
        #     form.save()
        return redirect("page_home")
    else:
        form = FormBlog(instance=blog)
        topics = Topic.objects.all()
        context = {"pagetitle": "Update Blog", "form": form, "topics": topics, "blog": blog}
        return render(request, "blog/form_blog.html", context)


@login_required(login_url="login")
def delete_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.user != blog.author:
        return HttpResponse("You are not allowed to edit or delete a blog created by others.")
    blog.delete()
    return redirect("page_home")


@login_required(login_url="login")
def delete_comment(request, blogid, pk):
    comment = Comment.objects.get(id=pk)
    if request.user != comment.author:
        return HttpResponse("You are not allowed to edit or delete a comment created by others.")
    comment.delete()
    return redirect("page-blog", pk=blogid)

@login_required(login_url='login')
def edit_userprofile(request):
    if request.method=='POST':
        form=FormUserProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=request.user.id)

    form=FormUserProfile(instance=request.user)
    context={'form':form}
    return render(request, 'blog/form_edit_userprofile.html', context)