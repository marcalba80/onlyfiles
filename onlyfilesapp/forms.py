from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from onlyfilesapp.models import UserRepo

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=100)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('user')
        password = cleaned_data.get('password')
        # Perform additional validation or logic here
        return cleaned_data
    
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']     

class CreateRepoForm(forms.Form):
    name = forms.CharField(max_length=50)

class AddFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept': '.txt'}))
