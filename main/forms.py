from django import forms
from . import models

BROWSE_BY=[
    ('U', 'University'),
    ('C', 'Categories')
]
class BrowseForm(forms.Form):
    browse_by = forms.ChoiceField(choices=BROWSE_BY)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Id'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))

