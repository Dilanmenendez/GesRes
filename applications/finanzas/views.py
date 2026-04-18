from django.shortcuts import render
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
# Create your views here.

# ------- Otras Views --------- #

class SuccessView(TemplateView):
    template_name = "finanzas/success.html"

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