from .models import Producto, Proveedor, Clasificacion, Compra, Consumo
from django import forms



#------- Form de Producto ----------#
class ProductoForm(forms.ModelForm):
    """Form definition for Producto."""

    class Meta:
        """Meta definition for Productoform."""

        model = Producto
        fields = (
            'nombre',
            'tipo',
            'precio',
            'proveedor',
            'clasificacion',
            'stock_actual',
            'stock_minimo',
            'descripcion',
        )

#------------ Form de Proveedor -----------#
class ProveedorForm(forms.ModelForm):
    """Form definition for Proveedor."""

    class Meta:
        """Meta definition for Proveedorform."""

        model = Proveedor
        fields = ('__all__')

#---------Form de Clasificacion ------------#
class ClasificacionForm(forms.ModelForm):
    """Form definition for Clasificacion."""

    class Meta:
        """Meta definition for Clasificacionform."""

        model = Clasificacion
        fields = ('nombre',)

# ---------------- Form de Compra ------------------#
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = (
            'producto',
            'cantidad',
        )
        

# ---------------- Form de Consumo ------------------#
class ConsumoForm(forms.ModelForm):
    class Meta:
        model = Consumo
        fields = (
            'producto',
            'cantidad',
            'motivo',
        )