from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator
from .models import User, Poster
import hashlib
import requests


def delSes(request, session_name=str):
    yes = False
    if request.session.get(session_name):
        yes = True
        del request.session[session_name]
    return yes


def index(request):
    if request.session.get('user_id') and not (User.objects.filter(id=request.session.get('user_id'))): return redirect('profile')
    user = None
    if User.objects.filter(id=request.session.get('user_id')):
        user = User.objects.get(pk=request.session['user_id'])
    posts = Poster.objects.order_by('-id')
    paginator = Paginator(posts, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/index.html', {'posts': page_obj, 'user': user})

def del_usr(request):
    if User.objects.filter(id=request.session.get('user_id')):
        user = User.objects.get(pk=request.session['user_id'])
        user.delete()
    return redirect('logout')


def user(request, id):
    if request.session.get('user_id') == id:
        return redirect('profile')
    if User.objects.filter(id=id):
        user = User.objects.get(pk=id)
        posts = Poster.objects.filter(user=user).order_by('-id')
        return render(request, 'main/user.html', {'user': user, 'posts': posts, 'session_user': request.session.get('user_id')})
    return redirect('index')

def addpost(request):
    if request.session.get('user_id'):
        user = User.objects.get(pk=request.session.get('user_id'))
        error = None
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            url = request.POST.get('url')
            try:
                requests.get(url)
                Poster.objects.create(
                    user=user, title=title, content=content, url=url)
                return redirect('profile')
            except:
                error = 'url is invalid'
        return render(request, 'main/add_post.html', {'error': error})
    return redirect('login')


def edit(request, id):
    error = None
    if Poster.objects.filter(pk=id) and request.session['user_id']:
        poster = Poster.objects.get(pk=id)
        if poster.user == User.objects.get(pk=request.session['user_id']):
            if request.method == 'POST':
                title = request.POST.get('title')
                content = request.POST.get('content')
                url = request.POST.get('url')
                try:
                    requests.get(url)
                    poster.title = title
                    poster.content = content
                    poster.url = url
                    poster.save()
                    return redirect('profile')
                except:
                    error = 'url is invalid'
            return render(request, 'main/edit.html', {'poster': poster, 'error': error})
    return redirect('profile')

def profile(request):
    if request.session.get('user_id') and not (User.objects.filter(id=request.session.get('user_id'))): return redirect('profile')
    posts = None
    error = None
    user = User.objects.get(pk=request.session.get('user_id')) if request.session.get('user_id') else None
    posts = Poster.objects.filter(user=user).order_by('-id')
    if not user: return redirect('login')
    return render(request, 'main/profile.html', {'user': user, 'posts': posts, 'error': error})


def registration(request):
    if request.session.get('user_id') and not (User.objects.filter(id=request.session.get('user_id'))): return redirect('profile')
    if request.session.get('user_id'):
        return redirect('profile')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if not User.objects.filter(username=username):
            if cpassword == password:
                password = hashlib.md5(cpassword.encode()).hexdigest()
                user = User.objects.create(
                    username=username, password=password)
                request.session['user_id'] = user.id
                return redirect('profile')
            else:
                error = 'Password is invalid'
        else:
            error = 'This user has been registered'
    return render(request, 'main/registration.html', {'error': error})


def login(request):
    if request.session.get('user_id'):
        return redirect('profile')
    error = 'You has been logined' if request.session.get('user_id') else None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = hashlib.md5(request.POST.get(
            'password').encode()).hexdigest()
        if User.objects.filter(username=username, password=password):
            request.session['user_id'] = User.objects.get(
                username=username, password=password).id
            return redirect('profile')
        else:
            error = 'User is not found'
    return render(request, 'main/login.html', {'error': error})


def logout(request):
    delSes(request, 'user_id')
    return redirect('profile')

def del_post(request, id):
    if request.session.get('user_id') and Poster.objects.filter(id=id):
        poster = Poster.objects.get(id=id)
        if User.objects.get(pk=request.session['user_id']) == poster.user:
            poster.delete()
    return redirect('profile')