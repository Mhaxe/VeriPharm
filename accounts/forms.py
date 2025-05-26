from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
