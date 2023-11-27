from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("This is the home page")
    return render(request, 'index.html')

def signup(request):
    # return HttpResponse("This is the signup page")
    return render(request, 'signup.html')


def login(request):
    # return HttpResponse("This is the login page")
    return render(request, 'login.html')

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

