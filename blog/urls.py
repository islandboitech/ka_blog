from django.urls import path
from .views import blogs, blog

urlpatterns = [
    path("blogs/", blogs, name="page_blogs"),
    path("blog/<int:pk>/", blog, name="page_blog"),
]
