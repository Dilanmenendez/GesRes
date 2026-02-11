from .models import Producto, Proveedor, Clasificacion
from django import forms



#------- Form de Producto ----------#
class ProductoForm(forms.ModelForm):
    """Form definition for Producto."""

    class Meta:
        """Meta definition for Productoform."""

        model = Producto
        fields = ('nombre',
                  'precio',
                  'proveedor',
                  'clasificacion',
                  'stock_minimo',
                  'descripcion',)
        
        widgets = {'',}

#------------ Form de Proveedor -----------#
class ProveedorForm(forms.ModelForm):
    """Form definition for Proveedor."""

    class Meta:
        """Meta definition for Proveedorform."""

        model = Proveedor
        fields = ('__all__',)

#---------Form de Clasificacion ------------#
class ClasificacionForm(forms.ModelForm):
    """Form definition for Clasificacion."""

    class Meta:
        """Meta definition for Clasificacionform."""

        model = Clasificacion
        fields = ('nombre',)
