from django.contrib import admin
from django.urls import include, path
from onlyfilesapp.views import index, login, signup, repository, createRepository, addUser

urlpatterns = [
    path('', index, name='index'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('repository', repository, name='repository'),
    path('createRepository', createRepository, name='createRepository'),
    path('addUser', addUser, name='addUser')
]

