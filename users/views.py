from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    return render(request, 'users/register.html')

def user_login(request):
    return render(request, 'users/login.html')

def user_logout(request):
    return redirect('home')

def profile(request):
    return render(request, 'users/profile.html')
