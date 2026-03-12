from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from .models import *
# Create your views here.

# ------- Otras Views --------- #
class InicioView(TemplateView):
    template_name = 'ventas/inicio.html'


# -------- Venta Views --------- # 


class VentaListView(ListView):
    model = Venta
    template_name = "ventas/list_all_ventas.html"
    paginate_by = 4

    def get_queryset(self):
        fecha = self.request.GET.get("fecha", "")
        id = self.request.GET.get("id", "")

        if fecha:
            return Venta.objects.buscar_venta_fecha(fecha)
        return Venta.objects.buscar_fecha_id(id)
    
# -------- Plato Views --------- #


class PlatoListView(ListView):
    model = Plato
    template_name = "ventas/list_all_platos.html"
    paginate_by = 4

    def get_queryset(self):
        kword = self.request.GET.get("kword", "")
        id = self.request.GET.get("id", "")

        if id:
            return Plato.objects.buscar_plato_id(id)
        return Plato.objects.buscar_plato_kword(kword)