from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
  age=forms.CharField(widget=forms.TextInput(attrs={'type':'number'}),required=True)
  email=forms.EmailField(required=True)
  phoneno=forms.CharField(widget=forms.TextInput(attrs={'type':'number'}),required=True)
  address=forms.CharField(max_length=100, required=True)

  class Meta:
    model=User
    fields=('username', 'password1', 'password2', 'first_name', 'last_name', 'age', 'email', 'phoneno', 'address')