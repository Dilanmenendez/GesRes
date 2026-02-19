from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, DeleteView, UpdateView, DetailView
from .models import Producto, Clasificacion, Proveedor
from .forms import ProductoForm, ClasificacionForm, ProveedorForm   
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError, F  
# Create your views here.

#------------- Producto Views ---------------#

class ProductoListView(ListView):
    model = Producto
    template_name = "stock/list_all_producto.html"
    paginate_by = 4

    def get_queryset(self):
        palabra_clave = self.request.GET.get('kword', "")
        producto_id = self.request.GET.get('id', "")
        clasificacion_id = self.kwargs.get('clasificacion_id')
        
        if producto_id:
            return Producto.objects.buscar_producto_id(producto_id)
        
        if clasificacion_id:
            return Producto.objects.filter(
                clasificacion_id = clasificacion_id).order_by('id')
        
        if palabra_clave in ['mp', 'pt', 'sc']:
            return Producto.objects.buscar_producto_tipo(palabra_clave)
        
        return Producto.objects.buscar_producto(palabra_clave)
            


class ProductoCreateView(CreateView):
    model = Producto
    template_name = "stock/add_producto.html"
    form_class = ProductoForm
    success_url = reverse_lazy('stock_app:success')


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = "stock/delete_producto.html"
    success_url = reverse_lazy('stock_app:success')


class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = "stock/update_producto.html"
    form_class = ProductoForm
    success_url = reverse_lazy('stock_app:success')


class ProductoDetailView(DetailView):
    model = Producto
    template_name = "stock/detail_producto.html"
    form_class = ProductoForm
    success_url = reverse_lazy('stock_app:success')

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


class ProveedorCreateView(CreateView):
    model = Proveedor
    template_name = "stock/add_proveedor.html"
    form_class = ProveedorForm
    success_url = reverse_lazy('stock_app:success')


class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = "stock/delete_proveedor.html"
    success_url = reverse_lazy('stock_app:success')


class ProveedorUpdateView(UpdateView):
    model = Proveedor
    template_name = "stock/update_proveedor.html"
    form_class = ProveedorForm
    success_url = reverse_lazy('stock_app:success')


class ProveedorDetailView(DetailView):
    model = Proveedor
    template_name = "stock/detail_proveedor.html"
    form_class = ProveedorForm
    success_url = reverse_lazy('stock_app:success')

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

class ClasificacionCreateView(CreateView):
    model = Clasificacion
    template_name = "stock/add_clasificacion.html"
    form_class = ClasificacionForm
    success_url = reverse_lazy('stock_app:success')


class ClasificacionDeleteView(DeleteView):
    model = Clasificacion
    template_name = "stock/delete_clasificacion.html"
    success_url = reverse_lazy('stock_app:success')


class ClasificacionUpdateView(UpdateView):
    model = Clasificacion
    template_name = "stock/update_clasificacion.html"
    form_class = ClasificacionForm
    success_url = reverse_lazy('stock_app:success')

#---------------- Otras Views -----------------#

class SuccessView(TemplateView):
    template_name = 'stock/success.html'

class InicioView(TemplateView):
    template_name = "inicio_stock.html"


class StockDashboardView(TemplateView):
    template_name = "stock/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_productos'] = Producto.objects.count()
        context['total_proveedores'] = Proveedor.objects.count()
        context['total_clasificaciones'] = Clasificacion.objects.count()
        context['low_stock_count'] = Producto.objects.filter(
            stock_actual__lte=F('stock_minimo')
            ).count()
        context['low_stock_items'] = Producto.objects.filter(
            stock_actual__lte=F('stock_minimo')
            ).order_by('stock_actual')[:6]
        return context
