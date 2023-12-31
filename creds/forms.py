from django.forms import ModelForm
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User

class userRegistrationForm(UserCreationForm):
    class Meta:
        model= User
        fields=['username', 'email', 'password1', 'password2']

class FormUserProfile(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','username', 'name', 'email', 'bio']
