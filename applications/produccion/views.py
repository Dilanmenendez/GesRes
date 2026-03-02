from django.utils import timezone
from django.shortcuts import redirect, render
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

class ProduccionDashboardView(TemplateView):
    template_name = "produccion/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        inicio_mes = now.replace(day=1)

        # Producciones del mes
        producciones_mes = Produccion.objects.filter(
            fecha__gte=inicio_mes
        ).select_related("producto")

        # Cantidad de producciones del mes
        context["cantidad_producciones_mes"] = producciones_mes.count()

        # Costo total del mes (sumado en Python)
        costo_total = 0
        for p in producciones_mes:
            costo_total += p.costo_total

        context["costo_total_mes"] = costo_total

        # Últimas 5 producciones
        context["ultimas_producciones"] = Produccion.objects.select_related(
            "producto"
        ).order_by("-fecha")[:5]

        # Producción agrupada por producto (simple)
        resumen_por_producto = {}

        for p in producciones_mes:
            nombre = p.producto.nombre

            if nombre not in resumen_por_producto:
                resumen_por_producto[nombre] = 0

            resumen_por_producto[nombre] += p.cantidad_producida

        context["resumen_por_producto"] = resumen_por_producto

        #cantidad de recetas
        context['cantidad_recetas'] = Receta.objects.count()

        return context
    
# ------ Producción Views --------- #

class ProduccionListView(ListView):
    model = Produccion
    template_name = "produccion/list_all_produccion.html"
    paginate_by = 4

    def get_queryset(self):
        palabra_clave = self.request.GET.get('kword', "")
        id = self.request.GET.get('id', "")

        if id:
            return Produccion.objects.buscar_produccion_id(id)
        
        return Produccion.objects.buscar_produccion(palabra_clave)


class ProduccionDetailView(DetailView):
    model = Produccion
    template_name = "produccion/detail_produccion.html"
    form_class = ProduccionForm

class ProduccionCreateView(CreateView):
    model = Produccion
    template_name = "produccion/create_produccion.html"
    form_class = ProduccionForm
    success_url = reverse_lazy('produccion_app:success')

class ProduccionAnulateView(DeleteView):
    model = Produccion
    template_name = 'produccion/anulate_produccion.html'
    form_class = ProduccionForm
    success_url = reverse_lazy('produccion_app:success')

    def post(self, request, *args, **kwargs):
        # accedemos al object a anular
        self.object = self.get_object()
        try:
            #llamamos a la funcion anular 
            self.object.anular()
        except ValidationError as e:
            return redirect(self.success_url)
        return redirect(self.success_url)
    
#------ Receta Views ---------#

class RecetaListView(ListView):
    model = Receta
    template_name = "produccion/list_all_receta.html"
    paginate_by = 4

    def get_queryset(self):
        palabra_clave = self.request.GET.get('kword', "")
        id = self.request.GET.get('id', "")

        if id:
            return Receta.objects.buscar_receta_id(id)
        return Receta.objects.buscar_receta(palabra_clave)
    
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

class RecetaUpdateView(UpdateView):
    model = Receta
    template_name = 'produccion/update_receta.html'
    form_class = RecetaForm
    success_url = reverse_lazy('produccion_app:all_receta')
    
#------ Ingredientes Receta Views ---------#

class IngredientesRecetaCreateView(CreateView):
    model = IngredientesReceta
    form_class = IngredientesRecetaForm
    template_name = "produccion/create_ingredientes_receta.html"

    def form_valid(self, form):
        # Aca creamos una instancia de la receta a la cual le vamos a agregar un ingrediente y validamos el form
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

class IngredientesRecetaUpdateView(UpdateView):
    model = IngredientesReceta
    template_name = "produccion/update_ingredientes_receta.html"
    form_class = IngredientesRecetaForm
    
    def get_success_url(self):
        return reverse(
            'produccion_app:detail_receta',
            kwargs={'pk': self.object.receta_id}
        )
    

