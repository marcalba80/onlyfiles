from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.generics import GenericAPIView

from onlyfilesapp.models import *
from onlyfilesapp.forms import *

# Create your views here.

@csrf_protect
def Register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)

@csrf_protect
def Login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect.')
            

    return render(request, 'login.html')

def Logout(request):

    logout(request)

    return redirect('login')

def Init(request):
    template = 'index.html'
    context = {
        
    }
    return render(request, template, context)

def Repo(request):
    template = 'repository.html'
    context = {
        "repos": User_Repository.objects.filter(userepo=request.user),
    }
    return render(request, template, context)

def File(request):
    template = 'Playlist/Playlists.html'
    context = {
        "files": Files_Repository.objects.filter(repository=request.GET.get('repo')),
        
    }
    return render(request, template, context)

@csrf_protect
def CreateRepo(request):
    template = 'createRepository.html'
    context = {
        # "repo_name": request.GET.get('repo_name'),
    }
    if request.method == 'POST':
        repo_name = request.POST.get('repo_name')
        repo = User_Repository.objects.filter(repository__name=repo_name, 
                                              userepo=request.user)
        if not repo:
            repo_inst = Repository(name=repo_name, master_key="")
            repo_inst.save()
            repouser_inst = User_Repository(userepo=request.user, repository=repo_inst, user_admin=True)
            repouser_inst.save()
        else:
            pass
        
    return render(request, template, context)

@csrf_protect
def AddUser(request):
    template = 'addUser.html'
    context = {
        "repo_name": request.GET.get('repo_name')
        
    }
    if request.method == 'POST':
        adduser_name = request.POST.get('add_user')
        repos_admin = User_Repository.objects.get(repository__name=context['repo_name'], 
                                              userepo=request.user, user_admin=True)
        repo_user = User_Repository.objects.filter(repository__name=context['repo_name'], 
                                              userepo__user__username=adduser_name)
        if repos_admin and not repo_user:
            repo_inst = repos_admin.repository
            repouser_inst = User_Repository(userepo=UserRepo.objects.get(user__username=adduser_name),
                                            repository=repo_inst, user_admin=False)
            repouser_inst.save()
        else:
            pass
    return render(request, template, context)

@csrf_protect
def AddFile(request):
    template = 'Playlist/Playlists.html'
    context = {
        "repo_name": request.GET.get('repo_name')
    }
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        filec = request.POST.get('file')
        repos_admin = User_Repository.objects.get(repository__name=context['repo_name'], 
                                              userepo=request.user, user_admin=True)
        repo_user = User_Repository.objects.filter(repository__name=context['repo_name'], 
                                              userepo__user__username=adduser_name)
        repo_file = Files_Repository.objects.filter(repository__name=context['repo_name'], 
                                              file__name=file_name)
        if repos_admin and not repo_file:
            file = Files(name=file_name, file=filec, cloud_id='')
            file.save()
            repofile_inst = Files_Repository(repository=repos_admin, file=file)
            repofile_inst.save()
        else:
            pass
    
    return render(request, template, context)

class SocialSignupAPIView(GenericAPIView):
    pass
