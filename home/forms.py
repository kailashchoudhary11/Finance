from statistics import mode
from django.forms import ModelForm, Form
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    # username = forms.CharField(max_length=150)
    # password1 = forms.CharField(widget= forms.PasswordInput())
    # password2 = forms.CharField(widget= forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']