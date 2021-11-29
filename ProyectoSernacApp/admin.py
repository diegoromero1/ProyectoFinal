from django.contrib import admin
from .models import *
from .models import FilesAdmin
from .forms import ElegirInlineFormset
# Register your models here.
admin.site.register(FilesAdmin)
admin.site.register(Profile)
admin.site.register(Post)

# Mauro Silva
class CategoriasAdmin(admin.ModelAdmin):
    search_fields = ['nombre', ]
    list_display = ['nombre', 'estado']

class Publicacionadmin(admin.ModelAdmin):
    list_display = ['titulo','Categorias','estado']
    list_filter = ['titulo','Categorias']
    model = Publicacion

admin.site.register(Categorias, CategoriasAdmin)
admin.site.register(Publicacion, Publicacionadmin)

# Diego Romero
# quiz
class ElegirRespuestasInline(admin.TabularInline):
    model = ElegirRespuesta
    can_delete = False
    max_num = ElegirRespuesta.MAXIMO_RESPUESTA
    min_num = ElegirRespuesta.MAXIMO_RESPUESTA
    formset = ElegirInlineFormset

class Comentariosadmin(admin.ModelAdmin):
    list_display = ['usuario','texto']
    list_filter = ['usuario']
    model = Comentarios

admin.site.register(Comentarios, Comentariosadmin)

class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (ElegirRespuestasInline,)
    list_display = ['texto', ]
    search_fields = ['texto', 'preguntas__texto']


class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido','quizUser']
    list_filter = ['quizUser', 'pregunta','respuesta','puntaje_obtenido']

    class Meta:
        model = PreguntasRespondidas

class ContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'mensaje', 'numero']
    list_filter = ['nombre']
    model = Contacto



admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(PreguntasRespondidas, PreguntasRespondidasAdmin)
admin.site.register(QuizUsuario)
# Diego Romero
