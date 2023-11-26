from django.conf.urls import url
from django.views.generic import TemplateView

from onlyfilesapp import views


urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^$', views.Init, name='init'),
    url(r'^signup/$', views.Register.as_view(), name="registre"),
    url(r'^Repo/$', views.Repo, name="Create_playlist"),

    url(r'^Repo/File/$', views.File, name='Edit_playlist'),
    url(r'^CreateRepo/$', views.CreateRepo, name='playlist'),

    url(r'^Repo/AddUser/$', views.AddUser, name="Delete_playlist"),
    # url(r'^Repo/UploadFile/$', views.Upload, name="Edit"),
    
]
