from django import forms
from .models import Plato, IngredientePlato, Venta, DetalleVenta

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'precio', 'activo']

class IngredientePlatoForm(forms.ModelForm):
    class Meta:
        model = IngredientePlato
        fields = ['plato', 'producto', 'cantidad']

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['total']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['venta', 'plato', 'cantidad']