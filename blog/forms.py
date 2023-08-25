from django.forms import ModelForm
from .models import Blog
from django.contrib.auth.models import User


class FormBlog(ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
        exclude = ["author", "participants"]


class FormUserProfile(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
