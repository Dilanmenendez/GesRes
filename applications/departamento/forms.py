from django import forms
from .models import Departamento

class DepartamentoAllForm(forms.ModelForm):
    """Form definition for Departamento."""

    class Meta:
        """Meta definition for Departamentoform."""

        model = Departamento
        fields = ('__all__')


