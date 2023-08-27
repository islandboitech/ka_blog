from django.db import models
from creds.models import User
# from django.contrib.auth.models import User

# Create your models here.



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.author.username, filename)

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # featured_image=models.ImageField(null=True, verbose_name='Featured image', upload_to ='uploads/% Y/% m/% d/')
    featured_image=models.ImageField(null=True, blank=True, verbose_name='Featured image', upload_to = user_directory_path)
    isupdated=models.BooleanField(default=False)

    """ class Meta:
        ordering = ["-updated", "-created"] """

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    isupdated=models.BooleanField(default=False)

    """  class Meta:
        ordering = ["-updated", "-created"]
    """
    def __str__(self):
        return self.comment[0:50]
