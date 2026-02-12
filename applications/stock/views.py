from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Producto, Clasificacion, Proveedor
# Create your views here.

#------------- Producto Views ---------------#

class ProductoListView(ListView):
    model = Producto
    template_name = "stock/list_all_producto.html"
    paginate_by = 4

    def get_queryset(self):
        palabra_clave = self.request.GET.get('kword', "")
        producto_id = self.request.GET.get('id', "")

        if producto_id:
            return Producto.objects.buscar_producto_id(producto_id)
        
        return Producto.objects.buscar_producto(palabra_clave)
    
#------------ Proveedor Views -----------------#

class ProveedorListView(ListView):
    model = Proveedor
    template_name = "stock/list_all_proveedor.html"
    paginate_by = 4

    def get_queryset(self):
        palabra_clave = self.request.GET.get('kword', "")
        proveedor_id = self.request.GET.get('id', "")

        if proveedor_id:
            return Proveedor.objects.buscar_proveedor_id(proveedor_id)
        
        return Proveedor.objects.buscar_proveedor(palabra_clave)
    
#------------ Clasificacion Views --------------#


class ClasificacionListView(ListView):
    model = Clasificacion
    template_name = "stock/list_all_clasificacion.html"
    paginate_by = 4

    def get_queryset(self):
        palabra_clave = self.request.GET.get('kword', "")
        clasificacion_id = self.request.GET.get('id', "")

        if clasificacion_id:
            return Clasificacion.objects.buscar_clasificacion_id(clasificacion_id)
        
        return Clasificacion.objects.buscar_clasificacion(palabra_clave)
    

#---------------- Otras Views -----------------#


class InicioView(TemplateView):
    template_name = "inicio_stock.html"
