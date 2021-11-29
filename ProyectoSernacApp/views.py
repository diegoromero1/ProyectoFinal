import os

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import query
from django.forms.widgets import CheckboxInput
from django.shortcuts import render, HttpResponse, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
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
from .models import Categorias, QuizUsuario, Pregunta, PreguntasRespondidas, Contacto, Publicacion, FilesAdmin, Post, \
    Comentarios
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from .forms import FormComentarios
from django.contrib.contenttypes.management import *


# Vistas de la pagina
def Detallepublicaciones(request, slug):
    publicacion = Publicacion.objects.get(slug=slug)
    return render(request, "ProyectoSernacApp/Publicaciones.html", {'detalle_publicacion': publicacion})


def Derechosydeberes(request):
    publicacion = Publicacion.objects.filter(estado=True,
                                             Categorias=Categorias.objects.get(nombre__iexact='Derechos y Deberes'))
    return render(request, "ProyectoSernacApp/Derechoydeberes.html", {'publicacion': publicacion})


def Educacionfinanciera(request):
    publicacion = Publicacion.objects.filter(estado=True,
                                             Categorias=Categorias.objects.get(nombre__iexact='Educacion Financiera'))
    return render(request, "ProyectoSernacApp/Educacionfinanciera.html", {'publicacion': publicacion})


def Consumoresponsable(request):
    publicacion = Publicacion.objects.filter(estado=True,
                                             Categorias=Categorias.objects.get(nombre__iexact='Consumo Responsable'))
    return render(request, "ProyectoSernacApp/Consumoresponsable.html", {'publicacion': publicacion})


def Jueguito(request):
    return render(request, "ProyectoSernacApp/Jueguito.html")


def Educacion(request):
    queryset = request.GET.get("buscar")
    publicacion = Publicacion.objects.filter(estado=True)

    if queryset:
        publicacion = Publicacion.objects.filter(
            Q(titulo__icontains=queryset) |
            Q(contenido__icontains=queryset)
        ).distinct()

    return render(request, "ProyectoSernacApp/Educacion.html", {'publicacion': publicacion})


def Login(request):
    archivo = FilesAdmin.objects.all()
    context = {
        'file': archivo
    }
    return render(request, 'ProyectoSernacApp/login.html', context)


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
        'form': CustomUserProfileForm(instance=usuario)
    }
    if request.method == 'POST':
        formulario = CustomUserProfileForm(data=request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Tus datos se han actualizado correctamente")
            return redirect(to='Educacion')

        data["form"] = formulario

    return render(request, "ProyectoSernacApp/Perfil.html", data)


##### DIEGO CUEVAS######
def send_email(mail, msj, nombre, numero):
    context = {'mail': mail,
               'msj': msj,
               'nombre': nombre,
               'numero': numero}
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
            send_email(mail, msj, nombre, numero)
        else:
            data["form"] = formulario

    return render(request, "ProyectoSernacApp/Consulta.html", data)


def misconsultas(request):
    name = request.user.username
    consultas = Contacto.objects.filter(nombre=name)

    context = {

        'consultas': consultas

    }

    return render(request, 'ProyectoSernacApp/misconsultas.html', context)


##### DIEGO CUEVAS######

# Diego Romero
# Descarga de archivos
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb')as fh:
            response = HttpResponse(fh.read(), content_type="adminupload")
            response['Content-Disposition'] = 'inline;filename=' + os.path.basename(file_path)
            return response

    raise Http404


def descarga(request):
    archivo = FilesAdmin.objects.all()
    context = {
        'file': archivo
    }
    return render(request, 'ProyectoSernacApp/descarga.html', context)


# Error 404 y 500
class Error404View(TemplateView):
    template_name = "Manejo_de_error/error_404.html"


class Error505View(TemplateView):
    template_name = "Manejo_de_error/error_500.html"

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()

        def view(request):
            r = v(request)
            r.render()
            return r

        return view


# Cometarios

def post(request):
    todos_los_post = Post.objects.all()

    context = {

        'post': todos_los_post

    }

    return render(request, 'comentarios/post.html', context)


def comentario_id(request, pk):
    instance = get_object_or_404(Comentarios, pk=pk)

    context = {

        "comentario": instance
    }

    return render(request, 'comentarios/instance.html', context)


def post_idd(request, pk):
    instance = get_object_or_404(Post, pk=pk)

    inicializar_datos = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }

    form = FormComentarios(request.POST or None, initial=inicializar_datos)

    if form.is_valid():

        content_type = ContentType.objects.get_for_model(Post)
        obj_id = form.cleaned_data.get("object_id")
        texto_data = form.cleaned_data.get("texto")

        padre_obj = None

        try:
            padre_id = int(request.POST.get("padre_identificador"))
        except:
            padre_id = None
        if padre_id:
            padre_qs = Comentarios.objects.filter(id=padre_id)
            if padre_qs.exists() and padre_qs.count() == 1:
                padre_obj = padre_qs.first()

        comentarios, created = Comentarios.objects.get_or_create(

            usuario=request.user,
            content_type=content_type,
            object_id=obj_id,
            texto=texto_data,
            padre=padre_obj

        )
        return HttpResponseRedirect(comentarios.content_object.get_absolute_url())

    ver_comentarios = instance.comentarios

    context = {

        'form': form,
        'instance': instance,
        'ver_comentarios': ver_comentarios

    }

    return render(request, 'comentarios/comentar.html', context)


def eliminarComentarios(request, id):
    # instance = get_object_or_404(Comentarios, id=id)
    try:
        instance = Comentarios.objects.get(id=id)

    except:
        raise Http404

    if instance.usuario != request.user:
        response = HttpResponse("Tu No tienes permiso para realizar esta accion")
        response.status_code = 403
        return response

    if request.method == "POST":
        padre_instance_url = instance.content_object.get_absolute_url()
        instance.delete()
        messages.success(request, "Esta accion ha eliminado el comentario")
        return HttpResponseRedirect(padre_instance_url)

    context = {

        'instance': instance

    }
    return render(request, 'comentarios/eliminar.html', context)


# Diego Romero


def Admin(request):
    return render(request, "ProyectoSernacApp/admin.html")
