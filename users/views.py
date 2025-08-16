from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse
from django.contrib.auth import login, logout


def log_in(request):
    form = LoginForm(data=request.POST or None)

    if form.is_valid():
        user = form.get_user()
        login(request,user)
        return redirect('app:home')
    return render(request, 'login.html', {'form':form})

def log_out(request):
    logout(request)
    return redirect('users:log_in')


def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('users:log_in')
    return render(request, 'register.html', {'form':form})

    


