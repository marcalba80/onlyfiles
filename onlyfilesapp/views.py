from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, UploadFileForm
from .helpers import handle_uploaded_file

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('loginPage')

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect.')
            # return render(request, 'login.html')

    return render(request, 'login.html')

def logoutUser(request):

    logout(request)

    return redirect('loginPage')

def repository(request):

    # TODO: Don't harcode it, some type of object with the files.
    context = {
        "repository": False,
    }
    return render(request, 'repository.html', context)

def createRepository(request):

    return render(request, 'createRepository.html')

def addUser(request):

    return render(request, 'addUser.html')

def uploadFile(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return redirect('repository/uploadFile')
    else:
        form = UploadFileForm()
    return render(request, "uploadFile.html", {"form": form})

