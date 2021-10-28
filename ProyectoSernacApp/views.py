from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import query
from django.forms.widgets import CheckboxInput
from django.shortcuts import render, HttpResponse, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404
from django.conf import settings
from django.template.loader import get_template
from django.contrib import messages

from .forms import CustomUserForm, CustomUserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import PasswordChangingForm, ContactoForm
from django.contrib.auth.views import PasswordChangeView
from .models import Categorias, QuizUsuario, Pregunta, PreguntasRespondidas, Contacto, Publicacion
from django.db.models import Q 

# Vistas de la pagina
def Detallepublicaciones(request, slug):
    publicacion = Publicacion.objects.get(slug = slug)
    return render(request, "ProyectoSernacApp/Publicaciones.html", {'detalle_publicacion':publicacion})

def Derechosydeberes(request):
    publicacion = Publicacion.objects.filter(estado = True, Categorias = Categorias.objects.get(nombre__iexact= 'Derechos y Deberes'))
    return render(request, "ProyectoSernacApp/Derechoydeberes.html", {'publicacion':publicacion})

def Educacionfinanciera(request):
    publicacion = Publicacion.objects.filter(estado = True, Categorias = Categorias.objects.get(nombre__iexact = 'Educacion Financiera'))
    return render(request, "ProyectoSernacApp/Educacionfinanciera.html", {'publicacion':publicacion})

def Consumoresponsable(request):
    publicacion = Publicacion.objects.filter(estado = True, Categorias = Categorias.objects.get(nombre__iexact = 'Consumo Responsable'))
    return render(request, "ProyectoSernacApp/Consumoresponsable.html", {'publicacion':publicacion})

def Jueguito(request):
    return render(request, "ProyectoSernacApp/Jueguito.html")

def Educacion(request):
    queryset = request.GET.get("buscar")
    publicacion = Publicacion.objects.filter(estado = True)

    if queryset:
        publicacion = Publicacion.objects.filter(
             Q(titulo__icontains= queryset) | 
             Q(contenido__icontains= queryset) 
        ).distinct()
        
    return render(request, "ProyectoSernacApp/Educacion.html", {'publicacion':publicacion})

def Login(request):
    return render(request, "ProyectoSernacApp/login.html")

# Diego Romero
# Registar quizUser
def Registro(request):
    titulo = 'Crear una cuenta'

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        context = {
            'form': form,
            'titulo': titulo,
        }
        if form.is_valid():
            form.save()
            return redirect(to='login')

    else:
        form = CustomUserForm()
        context = {
            'form': form,
            'titulo': titulo,
        }
    return render(request, "ProyectoSernacApp/Registro.html", context)


# Cambio de contrasena
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'accounts/password_success.html', {})


def tablero(request):
    total_usuarios_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:10]
    contador = total_usuarios_quiz.count()

    context = {

        'usuario_quiz': total_usuarios_quiz,
        'contar_user': contador
    }
    return render(request, 'play/tablero.html', context)


def jugar(request):
    QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
        respuesta_pk = request.POST.get('respuesta_pk')

        try:
            opcion_seleccionda = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
        except ObjectDoesNotExist:
            raise Http404

        QuizUser.validar_intento(pregunta_respondida, opcion_seleccionda)

        return redirect('resultado', pregunta_respondida.pk)

    else:
        pregunta = QuizUser.obtener_nuevas_preguntas()
        if pregunta is not None:
            QuizUser.crear_intentos(pregunta)
        context = {
            'pregunta': pregunta

        }
    return render(request, 'play/jugar.html', context)


def resultado_pregunta(request, pregunta_respondida_pk):
    respondida = get_object_or_404(PreguntasRespondidas, pk=pregunta_respondida_pk)

    context = {
        'respondida': respondida
    }
    return render(request, 'play/resultado.html', context)


# Diego Romero

def Perfil(request, id):
    usuario = User.objects.get(id=id)
    data = {
        'form': CustomUserProfileForm(instance = usuario)
    }
    if request.method == 'POST':
        formulario = CustomUserProfileForm(data=request.POST, instance = usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Tus datos se han actualizado correctamente")
            return redirect(to='Educacion')

        data["form"] = formulario
      
    return render(request,"ProyectoSernacApp/Perfil.html", data)

##### DIEGO CUEVAS######
def send_email(mail,msj,nombre,numero):

    context = {'mail':mail,
               'msj':msj,
               'nombre':nombre,
               'numero':numero}
    template = get_template("consultas/correo_respaldo.html")
    content = template.render(context)

    email = EmailMultiAlternatives(
            'Respaldo de consulta',
            'Sernac Educativo',
            settings.EMAIL_HOST_USER,
            [mail]


    )
    email.attach_alternative(content, 'text/html')
    email.send()

def consulta(request):
    data = {
        'form': ContactoForm()
    }
    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        msj = request.POST.get("mensaje")
        nombre = request.POST.get("nombre")
        mail = request.POST.get('mail')
        numero = request.POST.get('numero')

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Tu consulta se ha enviado correctamente")
            send_email(mail,msj,nombre,numero)
        else:
            data["form"]=formulario

    return render(request, "ProyectoSernacApp/Consulta.html", data)

##### DIEGO CUEVAS######

