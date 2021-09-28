from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxInput
from django.shortcuts import render, HttpResponse, redirect
from .forms import CustomUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User



#Vistas de la pagina
def Login(request):
    return render(request,"ProyectoSernacApp/Login.html")

def Inicio(request):
    return render(request,"ProyectoSernacApp/Inicio.html")

def Registro(request):
    data = {
        'form': CustomUserForm()
    }
    if request.method == 'POST':
        formulario = CustomUserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()

            #messages.success(request, "Te has registrado correctamente")
            return redirect(to='Inicio')


        data["form"] = formulario
      
    return render(request,"ProyectoSernacApp/Registro.html", data)


## CAMBIO DE CONTRASEÑA ##
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

