from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
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

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password','placeholder':'Ingrese su contraseña actual'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password','placeholder':'Ingrese nueva contraseña '}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password','placeholder':'Repita la contraseña '}))

    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')
