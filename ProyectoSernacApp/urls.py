from django.contrib import admin
from django.urls import path, include
from ProyectoSernacApp import views
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

from .views import Detallepublicaciones, PasswordsChangeView, jugar, resultado_pregunta, tablero
from . import views

urlpatterns = [

    path('', LoginView.as_view(template_name='ProyectoSernacApp/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='ProyectoSernacApp/logout.html'), name='logout'),
    path('accounts/profile/', views.Educacion, name = "Dentro"),   ### LUEGO DE INICIAR SESION MANDA A ACCOUNTS/PROFILE AJUSTÉ PARA IR A INICIO###
    path('Registro',views.Registro, name = "Registro"),
    path('password/',PasswordsChangeView.as_view(template_name='accounts/change_password.html'),name='password_change'),
    path('password_success',views.password_success,name="password_success"),
    path('Perfil',views.Perfil, name = "Perfil"),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_complete'),
    path('jugar/',jugar,name='jugar'),
    path('resultado/<int:pregunta_respondida_pk>/', resultado_pregunta, name='resultado'),
    path('tablero/', tablero, name='tablero'),
    path ('Consulta/', views.consulta, name = "Consulta"),
    path('Perfil/<id>/',views.Perfil, name = "Perfil"),
    path('Educacion/',views.Educacion, name = "Educacion"),
    path('Jueguito/',views.Jueguito, name = "Jueguito"),
    path('Derechosydeberes/',views.Derechosydeberes, name = "Derechosydeberes"),
    path('Educacionfinanciera/',views.Educacionfinanciera, name = "Educacionfinanciera"),
    path('Consumoresponsable/',views.Consumoresponsable, name = "Consumoresponsable"),
    path('<slug:slug>/',Detallepublicaciones, name = "Detalle_publicaciones"),







]