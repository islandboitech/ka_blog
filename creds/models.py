from django.db import models
from django.contrib.auth.models import AbstractUser


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.username, filename)


# Create your models here.
class User(AbstractUser):
    name=models.CharField(max_length=200, null=True, verbose_name='Full Name')
    email=models.EmailField(verbose_name="Email address", max_length=255, unique=True,)
    bio=models.TextField(null=True, blank=True)
    # avatar=models.ImageField(null=True, default='avatar.png')
    avatar=models.ImageField(null=True, verbose_name='Profile piture', upload_to = user_directory_path, default='avatar.png')

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]