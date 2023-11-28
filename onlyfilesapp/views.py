from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import FileResponse

from onlyfilesapp.models import *
from onlyfilesapp.forms import *

# Create your views here.

@csrf_protect
def Register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            userrepo = UserRepo(user=user, is_admin=False)
            userrepo.save()
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

def successoauth(request):
    if request.user.is_authenticated:
        userr = UserRepo.objects.filter(user=request.user)
        if not userr:
            userrepo = UserRepo(user=request.user, is_admin=False)
            userrepo.save()
    return redirect('home')

def Logout(request):

    logout(request)

    return redirect('login')

def Init(request):
    template = 'index.html'
    # print("User: " + str(request.user.is_authenticated))
    context = {
        
    }
    if request.user.is_authenticated:
        userr = User_Repository.objects.filter(userepo=UserRepo.objects.get(user=request.user))
        if userr: context.update({"repos": userr})
    
    return render(request, template, context)

# def Repo(request):
#     template = 'repository.html'
#     context = {
#         "repos": User_Repository.objects.filter(userepo=request.user),
#     }
#     return render(request, template, context)

def Repo(request):
    template = 'repository.html'
    context = {
            
    }
    if request.user.is_authenticated:
        reponame = request.GET.get('pk')
        user = UserRepo.objects.get(user=request.user)
        repos = User_Repository.objects.get(userepo=user, repository__pk=reponame)
        if repos:
            files = Files_Repository.objects.filter(repository=repos.repository)
            context.update(
                {
                "files": files if files else None,
                "repo": repos.repository,
                "is_admin": repos.user_admin,
                }
            )
    return render(request, template, context)

def GetFile(request):
    pk = request.GET.get('pk')
    userr = UserRepo.objects.get(user=request.user)
    file = Files.objects.get(pk=pk)
    filerepo = Files_Repository.objects.get(file=file)
    userepo = User_Repository.objects.get(userepo=userr, repository=filerepo.repository)
    if userepo:
        response = FileResponse(file.file)
        response['Content-Type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename="{}.txt"'.format(pk) # You can set custom filename, which will be visible for clients.
        return response

# def download(request, pk):
#     pass

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
        user = UserRepo.objects.get(userepo=request.user)
        if not repo:
            repo_inst = Repository(name=repo_name, master_key="")
            repo_inst.save()
            repouser_inst = User_Repository(userepo=user, repository=repo_inst, user_admin=True)
            repouser_inst.save()
        else:
            pass
        
    return render(request, template, context)

@csrf_protect
def AddUser(request):
    template = 'addUser.html'
    context = {
        "repo_name": request.GET.get('pk')
        
    }
    if request.method == 'POST':
        adduser_name = request.POST.get('username')
        userr = UserRepo.objects.get(user=request.user)
        repos_admin = User_Repository.objects.get(repository__pk=context['repo_name'], 
                                              userepo=userr, user_admin=True)
        repo_user = User_Repository.objects.filter(repository__pk=context['repo_name'], 
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
