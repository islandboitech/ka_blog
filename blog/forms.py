from django.forms import ModelForm
from .models import Blog


class FormBlog(ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
