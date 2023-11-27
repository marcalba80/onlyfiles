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
    template = 'home.html'
    context = {
        
    }
    return render(request, template, context)

def Repo(request):
    template = 'Playlist/Playlists.html'
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

def CreateRepo(request):
    template = 'createRepo.html'
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

def AddUser(request):
    template = 'Playlist/Playlists.html'
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
