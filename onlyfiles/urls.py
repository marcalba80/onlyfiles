from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
from onlyfilesapp import views

urlpatterns = [
    path('shoronpo/', admin.site.urls),
    path('', RedirectView.as_view(url='onlyfilesapp/'), name='home'),
    path('accounts/login/', views.Login, name='login'),
    path('accounts/signup/', views.Register, name='signup'),
    path('accounts/', include('allauth.urls')),
    path('login', views.Login, name='login'),
    path('logout', views.Logout, name='logout'),
    path('signup', views.Register, name="signup"),
    path('success/url/', views.successoauth, name='success'),
    path('onlyfilesapp/', include('onlyfilesapp.urls')),
]
