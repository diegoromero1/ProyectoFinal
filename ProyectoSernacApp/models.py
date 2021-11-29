from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


from django.conf import settings
import random


####Mauro Silva el que te lo pone#####
class Publicacion(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField('Titulo', max_length=90, blank=False, null=False)
    slug = models.CharField('Slug', max_length=100, blank=False, null=False)
    contenido = RichTextField('Contenido')
    Categorias = models.ForeignKey('Categorias', on_delete=models.CASCADE)
    estado = models.BooleanField('Categoria Activada/Categoria Desactivada', default=True)

    class Meta:
        verbose_name = 'Publicacion'
        verbose_name_plural = 'Publicaciones'

    def __str__(self):
        return self.titulo


class Categorias(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre de la categoria', max_length=100)
    estado = models.BooleanField('Categoria Activada/Categoria Desactivada', default=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre


#### Diego Cuevas ####
class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    mensaje = models.TextField()
    numero = models.IntegerField()

    def __str__(self):
        return self.mensaje


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Perfil de {self.user.username}'


# Diego Romero
class Post(models.Model):

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    tiempo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("post_idd", kwargs={"pk": self.pk})

    def comentarios(self):
        instance = self
        qs = Comentarios.objects.filtro_por_instancia(instance)
        return qs

    def get_content_type(self):
        content_type = ContentType.objects.get_for_model(Post)
        return content_type


def nueva_url(instance, url=None):
    slug = slugify(instance.texto)

    if url is not None:
        slug = url

    qs = Post.objects.filter(slug=slug).order_by("-id")

    if qs.exists():
        nueva_url_si = "%s-%s" % (slug, qs.first().id)
        return nueva_url(instance, url=nueva_url_si)
    return slug


def url_creada(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = nueva_url(instance)


pre_save.connect(url_creada, sender=Post)


class ComentariosManager(models.Manager):

    def filtro_por_instancia(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(ComentariosManager, self).filter(content_type=content_type, object_id=obj_id).filter(padre=None)
        return qs


class Comentarios(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    texto = models.TextField(verbose_name="Comentario")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = ComentariosManager()

    padre = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    tiempo = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-tiempo']

    def __str__(self):
        return self.texto[:15]

    def get_absolute_url(self):
        return reverse("comentario_id", kwargs={"pk": self.pk})

    def hijo(self):
        return Comentarios.objects.filter(padre=self)


# Diego Romero
# Creacion de quiz

class Pregunta(models.Model):
    NUMERO_DE_RESPUESTAS_PERMITIDAS = 1

    texto = models.TextField(verbose_name='Texto de la pregunta')
    max_puntaje = models.DecimalField(verbose_name='Maximo Puntaje', default=3, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.texto


class QuizUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puntaje_total = models.DecimalField(verbose_name='Puntaje total', default=0, decimal_places=2, max_digits=6)

    def crear_intentos(self, pregunta):
        intento = PreguntasRespondidas(pregunta=pregunta, quizUser=self)
        intento.save()

    def obtener_nuevas_preguntas(self):
        respondidas = PreguntasRespondidas.objects.filter(quizUser=self).values_list('pregunta__pk', flat=True)
        preguntas_restantes = Pregunta.objects.exclude(pk__in=respondidas)
        if not preguntas_restantes.exists():
            return None
        return random.choice(preguntas_restantes)

    def validar_intento(self, pregunta_respondida, respuesta_selecionada):
        if pregunta_respondida.pregunta_id != respuesta_selecionada.pregunta_id:
            return

        pregunta_respondida.respuesta_selecionada = respuesta_selecionada
        if respuesta_selecionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_selecionada.pregunta.max_puntaje
            pregunta_respondida.respuesta = respuesta_selecionada

        else:
            pregunta_respondida.respuesta = respuesta_selecionada

        pregunta_respondida.save()
        self.actualizar_puntaje()

    def actualizar_puntaje(self):
        puntaje_actualizado = self.intentos.filter(correcta=True).aggregate(models.Sum('puntaje_obtenido'))[
            'puntaje_obtenido__sum']

        self.puntaje_total = puntaje_actualizado
        self.save()


class ElegirRespuesta(models.Model):
    MAXIMO_RESPUESTA = 4
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    correcta = models.BooleanField(verbose_name='Es esta la pregunta correcta ', default=False, null=False)
    texto = models.TextField(verbose_name='Texto de la respuesta')

    def __str__(self):
        return self.texto


class PreguntasRespondidas(models.Model):

    quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='intentos')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, null=True)
    correcta = models.BooleanField(verbose_name='Es esta la respuesta correcta?', default=False, null=False)
    puntaje_obtenido = models.DecimalField(verbose_name='Puntaje Obtenido', default=0, decimal_places=2, max_digits=6)


# Descarga de archivos
class FilesAdmin(models.Model):
    adminupload = models.FileField(upload_to='media')
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

# Diego Romero
