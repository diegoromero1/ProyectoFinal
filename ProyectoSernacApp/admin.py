from django.contrib import admin
from .models import *
from .forms import ElegirInlineFormset

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Contacto)


#Mauro Silva   
class CategoriasAdmin(admin.ModelAdmin):
    search_fields = ['nombre',]
    list_display = ['nombre', 'estado']

admin.site.register(Categorias, CategoriasAdmin)
admin.site.register(Publicacion)

# Diego Romero
# quiz
class ElegirRespuestasInline(admin.TabularInline):
    model = ElegirRespuesta
    can_delete = False
    max_num = ElegirRespuesta.MAXIMO_RESPUESTA
    min_num = ElegirRespuesta.MAXIMO_RESPUESTA
    formset = ElegirInlineFormset


class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (ElegirRespuestasInline,)
    list_display = ['texto', ]
    search_fields = ['texto', 'preguntas__texto']


class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']

    class Meta:
        model = PreguntasRespondidas


admin.site.register(Pregunta, PreguntaAdmin)

admin.site.register(ElegirRespuesta)
admin.site.register(PreguntasRespondidas, PreguntasRespondidasAdmin)
admin.site.register(QuizUsuario)
# Diego Romero
