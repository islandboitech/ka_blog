from django.contrib import admin
from django.urls import path, include
from .views import loginUser, logoutUser, registerUser, userProfile, edit_userprofile

urlpatterns = [
    path("register/", registerUser, name="register"),
    path("login/", loginUser, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("user/profile/<int:pk>/", userProfile, name="user-profile"),
    path('user/editprofile/', edit_userprofile, name="edit-profile")
]
