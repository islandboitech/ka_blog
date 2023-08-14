from django.shortcuts import render


# Create your views here.
def blogs(request):
    return render(request, "blog/blogs.html")


def blog(request, pk):
    context = {"id": pk, "pagetitle": f"Blog Number {pk}"}
    return render(request, "blog/blog.html", context)
