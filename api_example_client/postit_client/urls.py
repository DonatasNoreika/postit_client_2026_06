from django.contrib import admin
from django.urls import path
from .views import posts, post, post_create, like_create

urlpatterns = [
    path("", posts, name="posts"),
    path("posts/<int:post_id>", post, name="post"),
    path("posts/new", post_create, name="post_create"),
    path("posts/<int:post_id>/like", like_create, name="post_like"),
]