from django.contrib import admin
from django.urls import include, path
from onlyfilesapp.views import index, loginPage, logoutUser, signup, repository, createRepository, addUser, uploadFile

urlpatterns = [
    path('', index, name='index'),
    path('signup', signup, name='signup'),
    path('login', loginPage, name='loginPage'),
    path('logout', logoutUser, name='logout'),
    path('repository', repository, name='repository'),
    path('repository/uploadFile', uploadFile, name='uploadFile'),
    path('createRepository', createRepository, name='createRepository'),
    path('addUser', addUser, name='addUser')
]

