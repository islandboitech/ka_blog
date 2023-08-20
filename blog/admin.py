from django.contrib import admin
from .models import Blog, Topic, Comment

# Register your models here.
admin.site.register(Blog)
admin.site.register(Topic)
admin.site.register(Comment)
