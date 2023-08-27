from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Blog, Topic, Comment
from .forms import FormBlog, FormComment
from django.db.models import Count, Q, Value
from django.contrib import messages
from datetime import date
# {{request.META.HTTP_REFERER}} # use this link to go back to the previous page (used in delete form in this system)


def getRecentActivity():
    # variable declarations
    # start: queryset UNION BLOG and COMMENT for recent activity
    qsBlog = Blog.objects.all().values('id', 'author', 'author__username', 'author__avatar', 'created', 'updated', 'isupdated', 'title').annotate(comment=Value(''), action1=Value('Posted a blog'), action2=Value('Edited a blog'))
    qsComment = Comment.objects.all().values('id', 'author', 'author__username', 'author__avatar', 'created', 'updated', 'isupdated', 'blog__title', 'comment').annotate(action1=Value('Wrote a comment to'), action2=Value('Edited a comment'))
    recent=qsBlog.union(qsComment).order_by('-updated', '-created')[:5]
    return recent
    # end: queryset UNION
    

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
    ).order_by('-updated', '-created')
    # recent_activity = Comment.objects.all()[:5] # show all messages regardless of topic
    # recent_activity = Comment.objects.all()[:5]  # show messages based on the topic selected
    recent=getRecentActivity()
    topics = Topic.objects.annotate(blogcount=Count("blog"))
    context = {"blogs": blogs, "topics": topics,  'recent':recent }
    return render(request, "blog/blogs.html", context)


def blog(request, pk):
    blog = Blog.objects.get(id=pk)
    topic=blog.topic
    if request.method == "POST":
        comment = Comment.objects.create(author=request.user, blog=blog, comment=request.POST.get("comment"))
        blog.participants.add(request.user)
        messages.success(request, f"Comment has been successfully created." )
        return redirect("page-blog", pk=blog.id)
    related_posts=Blog.objects.filter(topic__name__iexact=topic).exclude(id=pk)[:10]
    # topics = Topic.objects.annotate(blogcount=Count("blog"))
    participants = blog.participants.all()
    # comments = blog.comment_set.all().order_by("-created")
    comments = blog.comment_set.all()  # ordering is defined in the model directly
    recent=getRecentActivity()

    context = {
        "blog": blog,
        "comments": comments,
        "participants": participants,
        "related_posts": related_posts,
        "recent":recent
        # "topics": topics,
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
                description=request.POST.get('description'),
                featured_image= request.FILES['featured_image'] if request.FILES.get('featured_image') is not None else None
            )
            messages.success(request, f"You blog has been sucessfully published." )
            return redirect("page-blogs")
        except:
            messages.error(request, "An error occured while saving the blog.")
            return redirect("new-blog")
        # form = FormBlog(request.POST)
        # if form.is_valid():
        #     blog = form.save(commit=False)
        #     blog.author = request.user
        #     blog.save()
    else:
        recent=getRecentActivity()
        form = FormBlog()
        context = {"pagetitle": "Add New Blog", "form": form, "recent": recent}
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
        if request.FILES.get('featured_image') is not None:
            blog.featured_image= request.FILES['featured_image']
        else:
            blog.featured_image=None

        if not blog.isupdated:
            blog.isupdated=True
        blog.save()
        messages.success(request, f"Blog has been updated." )
        # form = FormBlog(request.POST, instance=blog)
        # if form.is_valid():
        #     form.save()
        return redirect("page-blogs")
    else:
        form = FormBlog(instance=blog)
        # topics = Topic.objects.all()
        related_posts=Blog.objects.filter(topic__name__iexact=blog.topic).exclude(id=pk)[:10]
        context = {"pagetitle": "Edit Blog", "form": form, "blog": blog, 'related_posts': related_posts, 'recent':getRecentActivity()}
        return render(request, "blog/form_blog.html", context)


@login_required(login_url="login")
def delete_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.user != blog.author:
        return HttpResponse("You are not allowed to edit or delete a blog created by others.")
    blog.delete()
    messages.success(request, f"Blog has been successfully deleted." )
    return redirect("page-blogs")


@login_required(login_url="login")
def delete_comment(request, blogid, pk):
    comment = Comment.objects.get(id=pk)
    if request.user != comment.author:
        return HttpResponse("You are not allowed to edit or delete a comment created by others.")
    comment.delete()
    messages.success(request, f"Comment has been successfully deleted." )
    return redirect("page-blog", blogid)

@login_required(login_url="login")
def update_comment(request, blogid, pk):
    blog = Blog.objects.get(id=blogid)
    comment = Comment.objects.get(id=pk)
    print(comment)
    if request.user != comment.author:
        return HttpResponse("You are not allowed to edit or update a comment created by others.")

    if request.method == "POST":
        comment.comment=request.POST.get('comment')

        if not comment.isupdated:
            comment.isupdated=True
        comment.save()
        messages.success(request, f"Comment has been updated." )
        # form = FormBlog(request.POST, instance=blog)
        # if form.is_valid():
        #     form.save()
        return redirect("page-blog", blogid)
    else:
        comments = blog.comment_set.all()
        form = FormComment(instance=comment)
        related_posts=Blog.objects.filter(topic__name__iexact=blog.topic).exclude(id=blogid)[:10]
        recent=getRecentActivity()
        context = {"form": form, "blog": blog, 'related_posts': related_posts, 'recent':recent, 'comments':comments, 'thecomment':comment}
        return render(request, "blog/blog.html", context)