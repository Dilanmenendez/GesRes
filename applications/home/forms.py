from django import forms
from .models import Prueba
class PruebaForm(forms.ModelForm):
    """Form definition for Prueba."""

    class Meta:
        """Meta definition for Pruebaform."""

        model = Prueba
        fields = ('titulo',
                  'subtitulo',
                  )
        #Los widgets los trae el form, y sire para personalizar nuestro form en el html
        #ej: poner un placeholder etc.
        #Estos se presentan en forma de diccionarios, la llave es el atributo a estilizar,
        #el valor, es el campo que vas a utilizar, ej: TextInput
        #attrs son los atributos que vas a ponrle, tambien estan en forma de diccionario, 
        #ej: attrs = {'placeholder': 'Ingresa un titulo}
        widgets = {
            'titulo': forms.TextInput(
                attrs = {
                    'placeholder': 'Ingresa un Titulo',
                }
            ),
            'subtitulo': forms.TextInput(
                attrs = {
                    'placeholder': 'Ingresa un Subtitulo'
                }
            ),
        }
        #asi como hay placeholder, hay muchos estilizadores mas, todo esta en la documentacion
        

    #Como hago para validar los datos que le llegan al form, django ya los valida normalmente
    #Pero si nos referimos a validaciones especificas, se hace asi:
    #siempre def clean_nombredevariable a validar(del fields)
    def clean_titulo(self):
        #con cleaned_data recuperamos el valor que queremos validar (en este caso 'titulo')
        titulo = self.cleaned_data['titulo']
        #y lueohacemos la logica de la vaidacion
        if len(titulo) < 6:
            #con forms.ValidateError podemos mandar un mensaje a la plantilla html si no
            #pasa la validacion
            raise forms.ValidationError('El titulo debe tener minimo 6 caracteres')
        #si sí pasa la validacion (no se ejecuta el ValidateError) retorna titulo
        return titulo


