from django import forms
from django.forms import inlineformset_factory
from .models import Plato, IngredientePlato, Venta, DetalleVenta

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'precio', 'activo']

class IngredientePlatoForm(forms.ModelForm):
    class Meta:
        model = IngredientePlato
        fields = ['plato', 'producto', 'cantidad']


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['plato', 'cantidad']

DetalleVentaFormSet = inlineformset_factory(
    Venta,
    DetalleVenta,
    form=DetalleVentaForm,
    extra=1,
    can_delete=True
)
