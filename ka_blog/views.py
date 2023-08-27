from django.shortcuts import render
from blog.models import Blog, Topic
from django.db.models import Count


""" def home(request):
    topics = Topic.objects.annotate(blogcount=Count("blog"))
    blogtotalcount = Blog.objects.all().count()
    latest_posts = Blog.objects.all().order_by('-updated', '-created')[:5]  # limit number of records

    context = {
        "blogs": latest_posts,
        "topics": topics,
        "blogtotalcount": blogtotalcount,
    }  # for sidebar display
    return render(request, "latest.html", context) """