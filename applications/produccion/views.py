from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView, DetailView
from .models import *
from .forms import *
# Create your views here.

# ------ Views Varios --------- #

class inicioView(TemplateView):
    template_name = "produccion/inicio.html"

# ------ Producción Views --------- #

class ProduccionListView(ListView):
    model = Produccion
    template_name = "produccion/list_all_produccion.html"
    paginate_by = 4

class ProduccionCreateView(CreateView):
    model = Produccion
    template_name = "produccion/add_produccion.html"
    form_class = ProduccionForm
    success_url = reverse_lazy('produccion_app:all_produccion')

#------ Receta Views ---------#

class RecetaListView(ListView):
    model = Receta
    template_name = "produccion/list_all_receta.html"
    paginate_by = 4

class RecetaCreateView(CreateView):
    model = Receta
    template_name = "produccion/add_receta.html"
    form_class = RecetaForm
    success_url = reverse_lazy('produccion_app:all_receta')

#------ Ingredientes Receta Views ---------#

class IngredientesRecetaCreateView(CreateView):
    model = IngredientesReceta
    template_name = "produccion/create_ingredientes_receta.html"
    form_class = IngredientesRecetaForm
    success_url = reverse_lazy('produccion_app:all_ingredientes_receta')