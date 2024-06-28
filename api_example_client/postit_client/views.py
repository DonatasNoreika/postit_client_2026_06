from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from .models import Profile

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


def like_create(request, post_id):
    headers = {'Authorization': token}
    r = requests.post(f"http://127.0.0.1:6500/posts/{post_id}/like", headers=headers)
    print(r.json())
    return redirect('posts')


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    user = User.objects.create_user(username=username, email=email, password=password)

                    data = {
                        "username": username,
                        'password': password,
                    }
                    r1 = requests.post("http://127.0.0.1:6500/signup/", data=data)
                    r2 = requests.post("http://127.0.0.1:6500/api-token-auth/", data=data)
                    token_dict = r2.json()
                    user = User.objects.filter(username=username)[0]
                    user.profile.token = token_dict['token']
                    user.save()

                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')