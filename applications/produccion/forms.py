from .models import Produccion, Receta, IngredientesReceta
from django import forms

#------- Form de Produccion ----------#
class ProduccionForm(forms.ModelForm):
    """Form definition for Produccion."""

    class Meta:
        """Meta definition for Produccionform."""

        model = Produccion
        fields = (
            'producto',
            'cantidad_producida',
        )

#------ Form de Receta ---------#
class RecetaForm(forms.ModelForm):
    """Form definition for Receta."""

    class Meta:
        """Meta definition for Recetaform."""

        model = Receta
        fields = ('producto_final',)
    
#------ Form de Ingredientes Receta ---------#
class IngredientesRecetaForm(forms.ModelForm):
    """Form definition for IngredientesReceta."""

    class Meta:
        """Meta definition for IngredientesRecetaform."""

        model = IngredientesReceta
        fields = (
            'producto',
            'cantidad',
        )