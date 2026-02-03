from django import forms
from .models import Departamento

#El FormView nos va a servir, por ejemplo, cuando necesitemos procesar datos para diferentes tablas,
#En un mismo template
class NewDepartamentoForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=True)
    apellido = forms.CharField(max_length=50, required=True)
    departamento = forms.CharField(max_length=50, required=True)
    short_name = forms.CharField(max_length=20, required=True)

class CreateDepartamentoForm(forms.ModelForm):
    """Form definition for Departamento."""

    class Meta:
        """Meta definition for Departamentoform."""

        model = Departamento
        fields = ('__all__')


class DepartamentoUpdateForm(forms.ModelForm):
    """Form definition for DepartamentoUpdate."""

    class Meta:
        """Meta definition for DepartamentoUpdateform."""

        model = Departamento
        fields = ('__all__')


