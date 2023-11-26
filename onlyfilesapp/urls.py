from django.contrib import admin
from django.urls import include, path
from onlyfilesapp.views import index, login, signup

urlpatterns = [
    path('', index, name='index'),
    path('signup', signup, name='signup'),
    path('login', login, name='login')
]

