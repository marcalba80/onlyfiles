from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=120)
    password = forms.CharField(max_length=100)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('user')
        password = cleaned_data.get('password')
        # Perform additional validation or logic here
        return cleaned_data