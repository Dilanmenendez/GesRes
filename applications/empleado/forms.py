from .models import Empleado, Habilidades, Trabajo
from django import forms
from ckeditor.widgets import CKEditorWidget 


class EmpleadoForm(forms.ModelForm):
    """Form definition for Empleado."""

    class Meta:
        """Meta definition for Empleadoform."""

        model = Empleado
        fields = (
            'first_name',
            'last_name',
            'job',
            'departamento',
            'habilidades',
            'hoja_vida',
            'cv',
            )
        
        widgets = {
            'habilidades' : forms.CheckboxSelectMultiple(),
            'hoja_vida' : CKEditorWidget(),
        }

class HabilidadesForm(forms.ModelForm):
    class Meta:
        model = Habilidades
        fields = ("habilidad",)

class TrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = ('puesto',
                  'sueldo',)
