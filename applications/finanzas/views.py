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

# ---------- GastoRecurrente Views ---------- #

class GastoRecurrenteListView(ListView):
    model = GastoRecurrente
    template_name = 'finanzas/list_all_gastos_recurrentes.html'
    context_object_name = 'gastos'

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