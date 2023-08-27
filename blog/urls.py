from django.urls import path
from .views import blogs, blog, new_blog, update_blog, delete_blog, delete_comment

urlpatterns = [
    path("", blogs, name="page-blogs"),
    path("blog/<int:pk>/", blog, name="page-blog"),
    path("blog/new/", new_blog, name="new-blog"),
    path("blog/update/<int:pk>/", update_blog, name="update-blog"),
    path("blog/delete/<int:pk>/", delete_blog, name="delete-blog"),
    path("blog/delete_comment/<int:blogid>/<int:pk>/",delete_comment,name="delete-comment"),
]
