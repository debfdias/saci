# login/views.py

from django.shortcuts import render, redirect

from . import models
from .models import User
from .forms import UserForm, RegisterForm
import hashlib


def index(request):
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', ''):
        return redirect("/index/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "dados incorretos"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:  
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "senha incorreta"
            except:
                message = "user nao encontrado"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', ''):
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "dados incorretos"
        if register_form.is_valid():  
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  
                message = "senhas diferentes"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  
                    message = 'usuario ja existe'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  
                    message = 'email ja usado'
                    return render(request, 'login/register.html', locals())


                new_user = User()
                new_user.name = username
                new_user.password = password1  
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', ''):
        return redirect('/index/')
    request.session.flush()

    return redirect('/index/')
