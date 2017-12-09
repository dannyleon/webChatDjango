# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from proyecto_final import settings
from .models import Chat
# Create your views here.
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# -*- coding: utf-8 -*-
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('chat/home2.html')
    else:
        form = UserCreationForm()
    return render(request, 'chat/signup.html', {'form': form})

def Login(request):
    next = request.GET.get('next', '/home2/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Account is not active at the moment.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    return render(request, "chat/login2.html", {'next': next})

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def Home(request):
    c = Chat.objects.all()

#<<<<<<< HEAD
    user = request.user.id
    nombre = request.user.username
    cant = Chat.objects.filter(user=user)
    print "-------------------------------"
    print nombre


    return render(request, "chat/home2.html", {'home': 'active', 'chat': c, 'nombre': nombre,'count': cant.count()})
#=======
    print c
    return render(request, "chat/home.html", {'home': 'active', 'chat': c})
#>>>>>>> cf5b351d99efe2045fe66ca6f3abf9c7bd96bd74

def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(user=request.user, message=msg)
        user = request.user.id
        cant = Chat.objects.filter(user=user)

        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.user.username, 'count': cant.count() })
    else:
        return HttpResponse('Request must be POST.')

def Messages(request):
    c = Chat.objects.all()
    return render(request, 'chat/messages.html', {'chat': c})
