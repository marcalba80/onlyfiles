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
    path('Signup/', views.Register.as_view(), name="signup"),
    path('Repo/', views.Repo, name="Repositories"),

    path('Repo/File/', views.File, name='Files'),
    path('CreateRepo/', views.CreateRepo, name='createRepo'),

    path('Repo/AddUser/', views.AddUser, name="AddUser"),
    path('Repo/AddFile/', views.AddFile, name="AddFile"),
    
]
