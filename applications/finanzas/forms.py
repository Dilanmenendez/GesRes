from django import forms
from .models import Cuenta, CategoriaMovimiento, GastoRecurrente, MovimientoFinanciero


# ------- Form de Cuenta ----------#
class CuentaForm(forms.ModelForm):
    """Form definition for Cuenta."""

    class Meta:
        """Meta definition for Cuentaform."""

        model = Cuenta
        fields = (
            'nombre',
            'tipo',
            'moneda',
            'descripcion',
            'activo',
        )


# ------- Form de CategoriaMovimiento ----------#
class CategoriaMovimientoForm(forms.ModelForm):
    """Form definition for CategoriaMovimiento."""

    class Meta:
        """Meta definition for CategoriaMovimientoform."""

        model = CategoriaMovimiento
        fields = (
            'nombre',
            'tipo',
            'descripcion',
        )


# ------- Form de GastoRecurrente ----------#
class GastoRecurrenteForm(forms.ModelForm):
    """Form definition for GastoRecurrente."""

    class Meta:
        """Meta definition for GastoRecurrenteform."""

        model = GastoRecurrente
        fields = (
            'nombre',
            'descripcion',
            'cuenta',
            'categoria',
            'monto_total',
            'meses',
            'fecha_inicio',
            'activo',
        )
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }


# ------- Form de MovimientoFinanciero ----------#
class MovimientoFinancieroForm(forms.ModelForm):
    """Form definition for MovimientoFinanciero."""

    class Meta:
        """Meta definition for MovimientoFinancieroform."""

        model = MovimientoFinanciero
        fields = (
            'cuenta',
            'categoria',
            'tipo',
            'monto',
            'descripcion',
            'documento',
            'fecha',
        )
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
