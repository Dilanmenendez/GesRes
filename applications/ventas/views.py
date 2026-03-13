from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import *
from .forms import *
# Create your views here.

# ------- Otras Views --------- #

class InicioView(TemplateView):
    template_name = 'ventas/inicio.html'

class SuccessView(TemplateView):
    template_name = "ventas/success.html"

# -------- Venta Views --------- # 

class VentaListView(ListView):
    model = Venta
    template_name = "ventas/list_all_ventas.html"
    paginate_by = 4

    def get_queryset(self):
        fecha = self.request.GET.get("fecha", "")
        id_venta = self.request.GET.get("key", "") # Evita usar 'id' como nombre de variable (es palabra reservada)

        if fecha:
            return Venta.objects.buscar_venta_fecha(fecha)
        
        if id_venta:
            return Venta.objects.buscar_venta_id(id_venta)
        
        # Si no hay ni fecha ni ID, devuelve la lista completa
        return Venta.objects.all().order_by('-fecha')


class VentaCreateView(CreateView):
    model = Venta
    template_name = "ventas/add_venta.html"
    fields = []

    success_url = reverse_lazy("ventas_app:success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["formset"] = DetalleVentaFormSet(self.request.POST)
        else:
            context["formset"] = DetalleVentaFormSet(queryset=DetalleVenta.objects.none())

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if formset.is_valid():
            self.object = form.save()

            formset.instance = self.object
            formset.save()

            return super().form_valid(form)

        return self.form_invalid(form)


class VentaDetailView(DetailView):
    model = Venta
    template_name = "ventas/detail_venta.html"

    def get_queryset(self):
        return Venta.objects.prefetch_related(
            "detalles__plato"
        )
    
# -------- Plato Views --------- #

class PlatoListView(ListView):
    model = Plato
    template_name = "ventas/list_all_platos.html"
    paginate_by = 4

    def get_queryset(self):
        kword = self.request.GET.get("kword", "")
        id = self.request.GET.get("key", "")

        if id:
            return Plato.objects.buscar_plato_id(id)
        return Plato.objects.buscar_plato_kword(kword)
    

class PlatoCreateView(CreateView):
    model = Plato
    template_name = "ventas/add_plato.html"
    form_class = PlatoForm
    success_url = reverse_lazy('ventas_app:success')


class PlatoDetailView(DetailView):
    model = Plato
    template_name = "ventas/detail_plato.html"


class PlatoUpdateView(UpdateView):
    model = Plato
    template_name = "ventas/update_plato.html"
    form_class = PlatoForm
    success_url = reverse_lazy('ventas_app:success')


# -------- IngredientePlato Views ----------- #

class IngredientePlatoCreateView(CreateView):
    model = IngredientePlato
    template_name = "ventas/add_ingrediente_plato.html"
    form_class = IngredientePlatoForm

    def form_valid(self, form):
        plato = get_object_or_404(Plato, pk=self.kwargs['pk'])
        form.instance.plato = plato
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'ventas_app:detail_plato',
            kwargs={'pk': self.kwargs['pk']}
        )

class IngredientePlatoUpdateView(UpdateView):
    model = IngredientePlato
    template_name = "ventas/update_ingrediente_plato.html"
    form_class = IngredientePlatoForm

    def get_success_url(self):
        return reverse(
            "ventas_app:detail_plato",
            kwargs={"pk": self.object.plato.id}
        )