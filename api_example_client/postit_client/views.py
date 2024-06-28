from django.shortcuts import render
import requests

# Create your views here.
def posts(request):
    r = requests.get("http://127.0.0.1:6500/posts/")
    posts_dict = r.json()
    return render(request, template_name="posts.html", context={"posts": posts_dict})

def post(request, post_id):
    r = requests.get(f"http://127.0.0.1:6500/posts/{post_id}")
    post_dict = r.json()
    return render(request, template_name="post.html", context={"post": post_dict})