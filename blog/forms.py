from django.forms import ModelForm
from .models import Blog, Comment
# from django.contrib.auth.models import User


class FormBlog(ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
        exclude = ["author", "participants"]

class FormComment(ModelForm):
    class Meta:
        model=Comment
        fields=['comment']
