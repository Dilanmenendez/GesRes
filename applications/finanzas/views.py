from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
# Create your views here.

# ------- Otras Views --------- #

class SuccessView(TemplateView):
    template_name = "finanzas/success.html"

class InicioView(TemplateView):
    template_name = 'finanzas/inicio.html'


class DashboardFinanzasView(TemplateView):
    template_name = 'finanzas/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cuentas = Cuenta.objects.filter(activo=True)
        movimientos = MovimientoFinanciero.objects.select_related('cuenta', 'categoria')

        hoy = timezone.localdate()
        inicio_mes = hoy.replace(day=1)
        movimientos_mes = movimientos.filter(fecha__date__gte=inicio_mes, fecha__date__lte=hoy)

        ingresos_mes = movimientos_mes.filter(tipo='I').aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
        egresos_mes = movimientos_mes.filter(tipo='E').aggregate(total=Sum('monto'))['total'] or Decimal('0.00')

        saldo_total = Decimal('0.00')
        for cuenta in cuentas:
            saldo_total += cuenta.saldo() if isinstance(cuenta.saldo(), Decimal) else Decimal(str(cuenta.saldo()))

        context.update({
            'total_cuentas': cuentas.count(),
            'saldo_total': saldo_total.quantize(Decimal('0.01')),
            'ingresos_mes': ingresos_mes.quantize(Decimal('0.01')),
            'egresos_mes': egresos_mes.quantize(Decimal('0.01')),
            'total_movimientos': movimientos.count(),
            'movimientos_recientes': movimientos.order_by('-fecha')[:5],
            'cuentas': cuentas.order_by('nombre')[:8],
            'balance_mes': (ingresos_mes - egresos_mes).quantize(Decimal('0.01')),
        })

        return context
    
# --------- Views de Cuenta --------- #

class CuentaListView(ListView):
    model = Cuenta
    template_name = 'finanzas/list_all_cuenta.html'
    context_object_name = 'cuentas'

class CuentaCreateView(CreateView):
    model = Cuenta
    template_name = 'finanzas/create_cuenta.html'
    form_class = CuentaForm
    success_url = reverse_lazy('finanzas_app:success')

class CuentaUpdateView(UpdateView):
    model = Cuenta
    template_name = 'finanzas/update_cuenta.html'
    form_class = CuentaForm
    success_url = reverse_lazy('finanzas_app:success')

class CuentaDeleteView(DeleteView):
    model = Cuenta
    template_name = 'finanzas/delete_cuenta.html'
    success_url = reverse_lazy('finanzas_app:success')

class CuentaDetailView(DetailView):
    model = Cuenta
    template_name = 'finanzas/detail_cuenta.html'
    context_object_name = 'cuenta'

# ---------- CategoriaMovimiento Views ---------- #

class CategoriaMovimientoListView(ListView):
    model = CategoriaMovimiento
    template_name = 'finanzas/list_all_categorias.html'
    context_object_name = 'categorias'

class CategoriaMovimientoCreateView(CreateView):
    model = CategoriaMovimiento
    template_name = 'finanzas/create_categoria.html'
    form_class = CategoriaMovimientoForm
    success_url = reverse_lazy('finanzas_app:success')


class CategoriaMovimientoDetailView(DetailView):
    model = CategoriaMovimiento
    template_name = 'finanzas/detail_categoria.html'
    context_object_name = 'categoria'


class CategoriaMovimientoUpdateView(UpdateView):
    model = CategoriaMovimiento
    template_name = 'finanzas/update_categoria.html'
    form_class = CategoriaMovimientoForm
    success_url = reverse_lazy('finanzas_app:all_categorias')


class CategoriaMovimientoDeleteView(DeleteView):
    model = CategoriaMovimiento
    template_name = 'finanzas/delete_categoria.html'
    success_url = reverse_lazy('finanzas_app:all_categorias')

# ---------- GastoRecurrente Views ---------- #

class GastoRecurrenteListView(ListView):
    model = GastoRecurrente
    template_name = 'finanzas/list_all_gastos_recurrentes.html'
    context_object_name = 'gastos'


class GastoRecurrenteDetailView(DetailView):
    model = GastoRecurrente
    template_name = 'finanzas/detail_gasto_recurrente.html'
    context_object_name = 'gasto'

class GastoRecurrenteCreateView(CreateView):
    model = GastoRecurrente
    template_name = 'finanzas/create_gasto_recurrente.html'
    form_class = GastoRecurrenteForm
    success_url = reverse_lazy('finanzas_app:success')

class GastoRecurrenteUpdateView(UpdateView):
    model = GastoRecurrente
    template_name = 'finanzas/update_gasto_recurrente.html'
    form_class = GastoRecurrenteForm
    success_url = reverse_lazy('finanzas_app:success')


class GastoRecurrenteDeleteView(DeleteView):
    model = GastoRecurrente
    template_name = 'finanzas/delete_gasto_recurrente.html'
    success_url = reverse_lazy('finanzas_app:all_gastos_recurrentes')

# -------------- MovimientoFinanciero Views -------------- #

class MovimientoFinancieroListView(ListView):
    model = MovimientoFinanciero
    template_name = 'finanzas/list_all_movimientos_financieros.html'
    context_object_name = 'movimientos'
    
class MovimientoFinancieroDetailView(DetailView):
    model = MovimientoFinanciero
    template_name = 'finanzas/detail_movimiento_financiero.html'
    context_object_name = 'movimiento'

class MovimientoFinancieroCreateView(CreateView):
    model = MovimientoFinanciero
    template_name = 'finanzas/create_movimiento_financiero.html'
    form_class = MovimientoFinancieroForm
    success_url = reverse_lazy('finanzas_app:success')

class MovimientoFinancieroAnularView(UpdateView):
    model = MovimientoFinanciero
    template_name = 'finanzas/anular_movimiento_financiero.html'
    fields = []
    success_url = reverse_lazy('finanzas_app:success')

    def form_valid(self, form):
        self.object.anular()
        return super().form_valid(form)