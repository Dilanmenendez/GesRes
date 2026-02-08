from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .forms import DepartamentoAllForm
from django.urls import reverse_lazy
from .models import Departamento

# Create your views here.

class DepartamentoListAllView(ListView):
    model = Departamento
    template_name = "departamento/list_all.html"
    paginate_by = 4

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')
        return Departamento.objects.buscar_departamento(palabra_clave)

class DepartamentoCreateView(CreateView):
    model = Departamento
    template_name = "departamento/create_departamento.html"
    form_class = DepartamentoAllForm
    success_url = reverse_lazy('persona_app:correcto')

class DepartamentoDeleteView(DeleteView):
    model = Departamento
    template_name = "departamento/delete_departamento.html"
    success_url = reverse_lazy('persona_app:correcto')


class DepartamentoUpdateView(UpdateView):
    model = Departamento
    template_name = "departamento/update_departamento.html"
    form_class = DepartamentoAllForm
    success_url = reverse_lazy('persona_app:correcto')