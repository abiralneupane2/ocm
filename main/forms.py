from django import forms
from django.forms import fields
from django.contrib.auth.models import User
from .models import Student



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Id'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user',]

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']