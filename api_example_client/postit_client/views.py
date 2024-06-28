from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests

token = "Token 1961a9e2cec10da70006b7ac51086a788ebb8882"
# Create your views here.
def posts(request):
    r = requests.get("http://127.0.0.1:6500/posts/")
    posts_dict = r.json()
    return render(request, template_name="posts.html", context={"posts": posts_dict})

def post(request, post_id):
    r = requests.get(f"http://127.0.0.1:6500/posts/{post_id}")
    post_dict = r.json()
    return render(request, template_name="post.html", context={"post": post_dict})

# @login_required
def post_create(request):
    if request.method == "POST":
        data = {
            "title": request.POST['title'],
            "body": request.POST['body'],
        }
        headers = {'Authorization': token}
        r = requests.post("http://127.0.0.1:6500/posts/", data=data, headers=headers)
        print(r.json())
        return redirect('posts')

    if request.method == "GET":
        return render(request, "post_create.html")