from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.widgets import CheckboxInput
from django.shortcuts import render, HttpResponse, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomUserForm, CustomUserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import PasswordChangingForm
from django.contrib.auth.views import PasswordChangeView



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

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request,'accounts/password_success.html', {})

def Perfil(request):
    data = {
        'form': CustomUserProfileForm()
    }
    if request.method == 'POST':
        formulario = CustomUserProfileForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()

            #messages.success(request, "Tus datos se han actualizado Correctamente")
            return redirect(to='Inicio')

        data["form"] = formulario
      
    return render(request,"ProyectoSernacApp/Perfil.html", data)
    