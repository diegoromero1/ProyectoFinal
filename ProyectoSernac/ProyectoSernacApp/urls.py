from django.contrib import admin
from django.urls import path, include
from ProyectoSernacApp import views
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

from .views import PasswordsChangeView
from . import views

urlpatterns = [

    path('', LoginView.as_view(template_name='ProyectoSernacApp/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='ProyectoSernacApp/logout.html'), name='logout'),
    path('Inicio/',views.Inicio, name = "Inicio"),
    path('accounts/profile/', views.Inicio, name = "Dentro"),   ### LUEGO DE INICIAR SESION MANDA A ACCOUNTS/PROFILE AJUSTÉ PARA IR A INICIO###
    path('Registro',views.Registro, name = "Registro"),
    path('password/',PasswordsChangeView.as_view(template_name='accounts/change_password.html'),name='password_change'),
    path('password_success',views.password_success,name="password_success"),

]