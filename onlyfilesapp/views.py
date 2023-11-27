from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from onlyfilesapp.models import *

# Create your views here.

class Register(CreateView):
    model = User
    template_name = "registration/registration.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

def Init(request):
    template = 'Playlist/Playlists.html'
    context = {

    }
    return render(request, template, context)

def Repo(request):
    template = 'Playlist/Playlists.html'
    context = {

    }
    return render(request, template, context)

def File(request):
    template = 'Playlist/Playlists.html'
    context = {
        
    }
    return render(request, template, context)

def CreateRepo(request):
    template = 'Playlist/Playlists.html'
    context = {
        
    }
    return render(request, template, context)

def AddUser(request):
    template = 'Playlist/Playlists.html'
    context = {
        
    }
    return render(request, template, context)
