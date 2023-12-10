from django.urls import path
from django.views.generic import TemplateView

from onlyfilesapp import views


urlpatterns = [
    path('', views.Init, name='init'),
    path('repository', views.Repo, name="Repositories"),
    path('deleteRepo', views.DeleteRepo, name="DeleteRepo"),

    path('getFile', views.GetFile, name='Files'),
    path('createRepository', views.CreateRepo, name='createRepo'),

    path('repository/addUser', views.AddUser, name="AddUser"),
    path('repository/addFile', views.AddFile, name="AddFile"),

    path('repository/deleteFile', views.DeleteFile, name="DeleteFile")
    
]
