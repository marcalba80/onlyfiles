from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from onlyfilesapp.models import *
from onlyfilesapp.forms import *
from onlyfilesapp.crypto import *
from onlyfilesapp.firebase import FIREBASE_BUCKET

import urllib, os
import magic
import uuid

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
    file_instance = Files.objects.get(pk=pk)
    filerepo = Files_Repository.objects.get(file=file_instance)
    userepo = User_Repository.objects.get(userepo=userr, repository=filerepo.repository)

    if userepo and file_instance:
        blob = FIREBASE_BUCKET.blob(str(filerepo.repository.pk) + "/" + file_instance.name)
        
        fcloud = open("./tmp/" + file_instance.name, "wb")
        blob.download_to_file(fcloud)
        fcloud.close()
        fcloud = open("./tmp/" + file_instance.name, "rb")
        # dec_file = decrypt_file(filerepo.repository.master_key, salt=file_instance.identifier.bytes, info=filerepo.repository.identifier.bytes, tag=file_instance.tag, file=file_instance.file)
        # print(fcloud)
        # response = FileResponse(file_instance.file)
        response = FileResponse(fcloud)
        response['Content-Type'] = 'text/plain'
        # namef = str(file.file.name).split('_')
        # name = '_'.join(namef[0:len(namef)-1])
        # response['Content-Disposition'] = 'attachment; filename="{}.txt"'.format(name) # You can set custom filename, which will be visible for clients.
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.name) # You can set custom filename, which will be visible for clients.
        # fcloud.close()
        # os.remove("./tmp/" + file.name)
        return response

@csrf_protect
def CreateRepo(request):
    template = 'createRepository.html'
    if request.method == 'POST':

        repo_name = request.POST.get('name')
        user = UserRepo.objects.get(user=request.user)
        repo = User_Repository.objects.filter(repository__name=repo_name, userepo=user, user_admin=True)

        if not repo:
            repo_inst = Repository(name=repo_name, master_key=generate_master_key_repository())
            repo_inst.save()
            repouser_inst = User_Repository(userepo=user, repository=repo_inst, user_admin=True)
            repouser_inst.save()
            return redirect('home')
        else:
            messages.error(request, "Repository already exists")
        
    form = CreateRepoForm()
    context = {
        'form': form,
    }
        
    return render(request, template, context)

@csrf_protect
def AddUser(request):
    template = "addUser.html"
    repopk = request.GET.get('pk')
    user = UserRepo.objects.get(user=request.user)
    
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
    
    if request.method == "POST":
        username = request.POST.get('username')
        repos_admin = User_Repository.objects.get(repository__pk=repopk, 
                                              userepo=user, user_admin=True)
        try:
            userradd = UserRepo.objects.get(user__username=username)
            repo_user = User_Repository.objects.get(repository__pk=repopk, userepo=userradd)
        except:
            useradd = None
            repo_user = None

        if not userradd: messages.error(request, "User does not exists")
        if repo_user: messages.error(request, "User already in the repository")
    
        if userradd and repos_admin and not repo_user:
            repo_inst = repos_admin.repository
            repouser_inst = User_Repository(userepo=userradd,
                                            repository=repo_inst, user_admin=False)
            repouser_inst.save()
            url = reverse('Repositories')
            params = urllib.parse.urlencode({"pk": repopk})
            return redirect(url + "?%s" % params)
            # return Repo(request)
    
    return render(request, template, context)

def validate_file_mimetype(file):
    accept = ['text/plain']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    return True if file_mime_type in accept else False

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

                if not f.name.endswith('.txt') or not validate_file_mimetype(f):
                    messages.error(request, "Unsupported file type")
                    context.update({'pk': repopk})
                    return render(request, template, context)
 
                repo = Repository.objects.get(pk=repopk)
                file_identifier = uuid.uuid4()
                enc_f, tag = encrypt_file(repo.master_key, salt=file_identifier.bytes, info=repo.identifier.bytes, file=f)

                # file_instance = Files(name=f.name, identifier=file_identifier, tag=tag)
                # file_instance.save()
                # file_instance.file.save(f.name, enc_f)
                # repof = Files_Repository(repository=repos.repository, file=file_instance)
                
                blob = FIREBASE_BUCKET.blob(repopk + "/" + f.name)
                blob.upload_from_file(enc_f, content_type=f.content_type)
                
                # file = Files(name=f.name, file=f, cloud_url=blob.public_url)
                file_instance = Files(name=f.name, cloud_url=blob.public_url, tag=tag, identifier=file_identifier)
                file_instance.save()
                repof = Files_Repository(repository=repos.repository, file=file_instance)
                repof.save()
                
                url = reverse('Repositories')
                params = urllib.parse.urlencode({"pk": repopk})
                return redirect(url + "?%s" % params)
    
    return render(request, template, context)


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
