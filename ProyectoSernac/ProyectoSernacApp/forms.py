from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserForm(UserCreationForm):

    class Meta:
        model= User
        fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        ]
    labels = {'username':'Nombre de usuario',
              'first_name':'Nombre',
              'last_name':'Apellidos',
              'email':'Correo',}
