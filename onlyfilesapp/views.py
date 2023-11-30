from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import FileResponse
from django.contrib.auth.decorators import login_required

from onlyfilesapp.models import *
from onlyfilesapp.forms import *

import urllib

# Create your views here.

@csrf_protect
def Register(request):
    if request.user.is_authenticated:
        return redirect('home')

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
    if request.user.is_authenticated:
        return redirect('home')

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
    if request.user.is_authenticated:
        template = 'index.html'
    else:
        template = 'index2.html'
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

@login_required(login_url='login')
def Repo(request):
    template = 'repository.html'
    context = {
            
    }
    if request.user.is_authenticated:

        repopk = request.GET.get('pk')
        user = UserRepo.objects.get(user=request.user)
        repos = User_Repository.objects.get(userepo=user, repository__pk=repopk)
        
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
        namef = str(file.file.name).split('_')
        name = '_'.join(namef[0:len(namef)-1])
        response['Content-Disposition'] = 'attachment; filename="{}.txt"'.format(name) # You can set custom filename, which will be visible for clients.
        return response

# def download(request, pk):
#     pass

@csrf_protect
def CreateRepo(request):
    template = 'createRepository.html'
    if request.method == 'POST':

        repo_name = request.POST.get('name')
        user = UserRepo.objects.get(user=request.user)
        repo = User_Repository.objects.filter(repository__name=repo_name, userepo=user)

        if not repo:
            repo_inst = Repository(name=repo_name, master_key="")
            repo_inst.save()
            repouser_inst = User_Repository(userepo=user, repository=repo_inst, user_admin=True)
            repouser_inst.save()
            return redirect('home')
        
    form = CreateRepoForm()
    context = {
        'form': form,
    }
        
    return render(request, template, context)

# def uploadFile(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             request.FILES["file"]
#             return redirect('repository')
    
#     form = UploadFileForm()
#     return render(request, "repository.html", {"form": form})

@csrf_protect
def AddUser(request):
    template = "addUser.html"
    repopk = request.GET.get('pk')
    user = UserRepo.objects.get(user=request.user)
    
    if request.method == "POST":
        username = request.POST.get('username')

        if not UserRepo.objects.filter(user__username=username):
            messages.error(request, f"User {username} doesn't exist")
            url = reverse('AddUser')
            params = urllib.parse.urlencode({"pk": repopk})
            return redirect(url + "?%s" % params)

        userradd = UserRepo.objects.get(user__username=username)
        repos_admin = User_Repository.objects.get(repository__pk=repopk, 
                                              userepo=user, user_admin=True)
        repo_user = User_Repository.objects.filter(repository__pk=repopk, 
                                              userepo=userradd)
        if userradd and repos_admin and not repo_user:
            repo_inst = repos_admin.repository
            repouser_inst = User_Repository(userepo=userradd,
                                            repository=repo_inst, user_admin=False)
            repouser_inst.save()
            url = reverse('Repositories')
            params = urllib.parse.urlencode({"pk": repopk})
            return redirect(url + "?%s" % params)
            # return Repo(request)
        else:
            messages.error(request, f"User {username} already in the repository")
     
    form = AddUserForm()
    context = {
        "form": form,
    }   
    if request.user.is_authenticated:            
        repos = User_Repository.objects.get(userepo=user, repository__pk=repopk)
        if repos:
            # files = Files_Repository.objects.filter(repository=repos.repository)
            context.update(
                {
                # "repo": repos.repository,
                "is_admin": repos.user_admin,
                }
            )
    
    return render(request, template, context)
    # template = 'addUser.html'
    # context = {
    #     "repo_name": request.GET.get('repo_name')
        
    # }
    # if request.method == 'POST':
    #     adduser_name = request.POST.get('add_user')
    #     repos_admin = User_Repository.objects.get(repository__name=context['repo_name'], 
    #                                           userepo=request.user, user_admin=True)
    #     repo_user = User_Repository.objects.filter(repository__name=context['repo_name'], 
    #                                           userepo__user__username=adduser_name)
    #     if repos_admin and not repo_user:
    #         repo_inst = repos_admin.repository
    #         repouser_inst = User_Repository(userepo=UserRepo.objects.get(user__username=adduser_name),
    #                                         repository=repo_inst, user_admin=False)
    #         repouser_inst.save()
    #     else:
    #         pass
    # return render(request, template, context)

@csrf_protect
def AddFile(request):
    template = "addFile.html"
    form = AddFileForm()
    context = {
        "form": form,
    }
        
    if request.user.is_authenticated:
        repopk = request.GET.get('pk')
        user = UserRepo.objects.get(user=request.user)
        repos = User_Repository.objects.get(userepo=user, repository__pk=repopk)
        if repos:
            # files = Files_Repository.objects.filter(repository=repos.repository)
            context.update(
                {
                # "repo": repos.repository,
                "is_admin": repos.user_admin,
                }
            )
        
        if request.method == "POST":
            form = AddFileForm(request.POST, request.FILES)
            if form.is_valid():
                # print(form.title)
                f = request.FILES['file']

                if not f.name.endswith('.txt'):
                    url = reverse('Repositories')
                    params = urllib.parse.urlencode({"pk": repopk})
                    return redirect(url + "?%s" % params)

                file = Files(name=f.name, file=f)
                file.save()
                repof = Files_Repository(repository=repos.repository, file=file)
                repof.save()
                # for chunk in f.chunks():
                #     print(chunk)
                url = reverse('Repositories')
                params = urllib.parse.urlencode({"pk": repopk})
                return redirect(url + "?%s" % params)
    
    return render(request, template, context)

    # template = 'Playlist/Playlists.html'
    # context = {
    #     "repo_name": request.GET.get('repo_name')
    # }
    # if request.method == 'POST':
    #     file_name = request.POST.get('file_name')
    #     filec = request.POST.get('file')
    #     repos_admin = User_Repository.objects.get(repository__name=context['repo_name'], 
    #                                           userepo=request.user, user_admin=True)
    #     repo_user = User_Repository.objects.filter(repository__name=context['repo_name'], 
    #                                           userepo__user__username=adduser_name)
    #     repo_file = Files_Repository.objects.filter(repository__name=context['repo_name'], 
    #                                           file__name=file_name)
    #     if repos_admin and not repo_file:
    #         file = Files(name=file_name, file=filec, cloud_id='')
    #         file.save()
    #         repofile_inst = Files_Repository(repository=repos_admin, file=file)
    #         repofile_inst.save()
    #     else:
    #         pass
    
    # return render(request, template, context)

def DeleteRepo(request):

    if request.user.is_authenticated:
        repopk = request.GET.get('pk')
        user = UserRepo.objects.get(user=request.user)
        user_repository = User_Repository.objects.get(userepo=user, repository__pk=repopk)

        if user_repository.user_admin:
            repo = Repository.objects.get(pk=repopk)

            files = Files_Repository.objects.filter(repository=user_repository.repository)

            for file in files:
                file.delete()

            repo.delete()
            users_repository = User_Repository.objects.filter(repository__pk=repopk)

            for user_repo in users_repository:
                user_repo.delete()

        return redirect('home')
    return redirect('home')


def DeleteFile(request):
    
    if request.user.is_authenticated:
        user = UserRepo.objects.get(user=request.user)
        filepk = request.GET.get('pk')
        file = Files.objects.get(pk=filepk)
        file_repository = Files_Repository.objects.get(file=file)
        repo = Repository.objects.get(pk=file_repository.repository.pk)

        user_repository = User_Repository.objects.get(userepo=user, repository__pk=repo.pk)

        if user_repository.user_admin:
            file.delete()
            file_repository.delete()

        url = reverse('Repositories')
        params = urllib.parse.urlencode({"pk": repo.pk})
        return redirect(url + "?%s" % params)
