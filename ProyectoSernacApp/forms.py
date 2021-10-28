from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Pregunta,ElegirRespuesta,PreguntasRespondidas,Contacto





#### Diego Cuevas #####
class ContactoForm(forms.ModelForm):

    class Meta:
        model=Contacto
        fields=["nombre",
                "mensaje",
                "numero"]


    labels = {'nombre': 'Nombre',
              'mensaje':'consulta',
              'numero':'numero'
                }



#Diego Romero
#Creacion de quizUser
class CustomUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2'
        ]
    labels = {'username':'Nombre de quizUser',
              'first_name':'Nombre',
              'last_name':'Apellidos',
              'email':'Correo',}
#Diego Romero


class CustomUserProfileForm(forms.ModelForm):
    
    class Meta:
        model= User
        fields = ['first_name','last_name','email',]
    labels = {'first_name':'Nombre',
              'last_name':'Apellidos',
              'email':'Correo',}              


#Diego Romero
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password','placeholder':'Ingrese su contraseña actual'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password','placeholder':'Ingrese nueva contraseña '}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password','placeholder':'Repita la contraseña '}))

    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')
#Diego Romero

class ElegirInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(ElegirInlineFormset, self).clean()

        respuesta_correcta = 0
        for formulario in self.forms:
            if not formulario.is_valid():
                return

            if formulario.cleaned_data and formulario.cleaned_data.get('correcta') is True:
                respuesta_correcta += 1
        try:
            assert respuesta_correcta == Pregunta.NUMERO_DE_RESPUESTAS_PERMITIDAS
        except AssertionError:
            raise forms.ValidationError('Exactamente solo una respuesta es permitida')