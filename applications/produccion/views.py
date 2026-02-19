from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView, DetailView
from .models import *
# Create your views here.

# ------ Views Varios --------- #

class inicioView(TemplateView):
    template_name = "produccion/inicio.html"

# ------ Producción Views --------- #

class ProduccionListView(ListView):
    model = Produccion
    template_name = "produccion/list_all_produccion.html"
    paginate_by = 4

#------ Receta Views ---------#

class RecetaListView(ListView):
    model = Receta
    template_name = "produccion/list_all_receta.html"
    paginate_by = 4

#------ Ingredientes Receta Views ---------#

class IngredientesRecetaListView(ListView):
    model = IngredientesReceta
    template_name = "produccion/list_all_ingredientes_receta.html"
    paginate_by = 4