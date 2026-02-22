from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView, DetailView
from .models import *
from .forms import *
# Create your views here.

# ------ Views Varios --------- #

class inicioView(TemplateView):
    template_name = "produccion/inicio.html"

class SuccessView(TemplateView):
    template_name = "produccion/success.html"

# ------ Producción Views --------- #

class ProduccionListView(ListView):
    model = Produccion
    template_name = "produccion/list_all_produccion.html"
    paginate_by = 4

class ProduccionCreateView(CreateView):
    model = Produccion
    template_name = "produccion/create_produccion.html"
    form_class = ProduccionForm
    success_url = reverse_lazy('produccion_app:create_produccion')

#------ Receta Views ---------#

class RecetaListView(ListView):
    model = Receta
    template_name = "produccion/list_all_receta.html"
    paginate_by = 4

class RecetaDetailView(DetailView):
    model = Receta
    template_name = "produccion/detail_receta.html"
    form_class = RecetaForm
    success_url = reverse_lazy('produccion_app:all_receta')

class RecetaCreateView(CreateView):
    model = Receta
    template_name = "produccion/create_receta.html"
    form_class = RecetaForm
    success_url = reverse_lazy('produccion_app:success')

class RecetaDeleteView(DeleteView):
    model = Receta
    template_name = "produccion/delete_receta.html"
    success_url = reverse_lazy('produccion_app:success')

#------ Ingredientes Receta Views ---------#

class IngredientesRecetaCreateView(CreateView):
    model = IngredientesReceta
    form_class = IngredientesRecetaForm
    template_name = "produccion/create_ingredientes_receta.html"

    def form_valid(self, form):
        # Aca creamos una instancia de la receta a la cual le vamos a agregar un ingrediente
        form.instance.receta_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'produccion_app:detail_receta',
            kwargs={'pk': self.kwargs['pk']}
        )

class IngredientesRecetaDeleteView(DeleteView):
    model = IngredientesReceta
    template_name = "produccion/delete_ingredientes_receta.html"

    def get_success_url(self):
        return reverse(
            'produccion_app:detail_receta',
            kwargs={'pk': self.object.receta_id}
        )