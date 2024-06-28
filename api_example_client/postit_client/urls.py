from django.contrib import admin
from django.urls import path
from .views import posts, post

urlpatterns = [
    path("", posts, name="posts"),
    path("posts/<int:post_id>", post, name="post"),
]