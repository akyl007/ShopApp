import requests
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import request
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import CustomRegistrationForm, CustomLoginForm
from .models import CustomUserManager


def registration_view(http_request):
    if http_request.method == 'POST':
        print('starting registration--------------------------------------------------------------------')
        form = CustomRegistrationForm(http_request.POST)
        print('chosen form registration--------------------------------------------------------------------')
        if form.is_valid():
            print('form is valid--------------------------------------------------------------------')
            user = form.save()
            user.save()
            username = http_request.session.get('username', 'Guest')
            if user:
                loginUser(http_request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                return render(http_request, 'main/index.html', {'username': username})
    else:
        print('form is not valid--------------------------------------------------------------------')
        form = CustomRegistrationForm()

    data = {'form': form}
    return render(http_request, 'registration/signup.html', data)


def login_view(http_request):
    print('login starting-----------------------------------------------------------------------')
    if http_request.method == 'POST':
        print('method post----------------------------------------------------------------------')
        username = http_request.POST['username']
        password = http_request.POST['password']
        return loginUser(http_request, username, password)
    else:
        form = CustomLoginForm()

    data = {'form': form}

    return render(http_request, 'registration/login.html', data)


def loginUser(http_request, username, password):
    response = generate_token(username, password)  # Токены JWT

    user = authenticate(http_request, username=username, password=password)
    if user:
        print('User authenticated----------------------------------------------------------------')

        auth_login(http_request, user)

        http_request.session['username'] = user.username

        http_request.session['access_token'] = response.get('access')
        http_request.session['refresh_token'] = response.get('refresh')

        return redirect('main:index')  # Перенаправление на защищенный ресурс

    else:
        return HttpResponse('Invalid credentials', status=401)


def logout_view(http_request):
    if http_request.user.is_authenticated:
        http_request.session.pop('access_token', None)
        http_request.session.pop('refresh_token', None)
        auth_logout(http_request)
        return render(http_request, 'main/index.html')

    return redirect('main:index')


def generate_token(username, password):
    token_url = 'http://127.0.0.1:8000/api/token/'  # URL для получения токенов
    response = requests.post(token_url, data={'username': username, 'password': password})

    if response.status_code == 200:
        return response.json()  # Возвращаем словарь с токенами
    return {}
