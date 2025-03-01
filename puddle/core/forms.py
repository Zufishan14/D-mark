from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'class': 'w-full py-4 px-6 rounded'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Email', 'class': 'w-full py-4 px-6 rounded'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'w-full py-4 px-6 rounded'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password', 'class': 'w-full py-4 px-6 rounded'}))  
    