from django.urls import path
from django.views.generic import TemplateView

from onlyfilesapp import views


urlpatterns = [
    # path(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    # path(r'^$', views.Init, name='init'),
    # path(r'^signup/$', views.Register.as_view(), name="registre"),
    # path(r'^Repo/$', views.Repo, name="Create_playlist"),

    # path(r'^Repo/File/$', views.File, name='Edit_playlist'),
    # path(r'^CreateRepo/$', views.CreateRepo, name='playlist'),

    # path(r'^Repo/AddUser/$', views.AddUser, name="Delete_playlist"),
    # path(r'^Repo/UploadFile/$', views.Upload, name="Edit"),

    path('', views.Init, name='init'),
    path('signup', views.Register.as_view(), name="signup"),
    path('repository', views.Repo, name="Repositories"),

    path('repository/file', views.File, name='Files'),
    path('createRepository', views.CreateRepo, name='createRepo'),

    path('repository/addUser', views.AddUser, name="AddUser"),
    path('repository/addFile', views.AddFile, name="AddFile"),
    
]
