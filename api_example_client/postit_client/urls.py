from django.contrib import admin
from django.urls import path
from .views import posts, post, post_create

urlpatterns = [
    path("", posts, name="posts"),
    path("posts/<int:post_id>", post, name="post"),
    path("posts/new", post_create, name="post_create"),
]