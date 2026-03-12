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
        id_venta = self.request.GET.get("key", "") # Evita usar 'id' como nombre de variable (es palabra reservada)

        if fecha:
            return Venta.objects.buscar_venta_fecha(fecha)
        
        if id_venta:
            return Venta.objects.buscar_venta_id(id_venta)
        
        # Si no hay ni fecha ni ID, devuelve la lista completa
        return Venta.objects.all().order_by('-fecha')
    
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