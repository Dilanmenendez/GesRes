from django.contrib import admin
from django.urls import path
from . import views


app_name = 'stock_app'

urlpatterns = [
     path('', 
          views.InicioView.as_view(), 
          name='Inicio'),

     path('success_url', 
          views.SuccessView.as_view(), 
          name='success'),

     # ----- Path Productos ----- #
     path('lista_all_productos/', 
          views.ProductoListView.as_view(), 
          name='all_productos'),

     path('add-producto/', 
          views.ProductoCreateView.as_view(), 
          name='add_producto'),

     path('productos/clasificacion/<clasificacion_id>/', 
          views.ProductoListView.as_view(), 
          name='productos_por_clasificacion'),

     path('delete-producto/<pk>/',
          views.ProductoDeleteView.as_view(),
          name='delete_producto'),

     # -------- Path Proveedores --------- #

     path('lista_all_proveedores/', 
          views.ProveedorListView.as_view(), 
          name='all_proveedores'),
     
     path('add-proveedor/', 
          views.ProveedorCreateView.as_view(),
          name='add_proveedor'),

     path('delete-proveedor/<pk>',
          views.ProveedorDeleteView.as_view(),
          name='delete_proveedor'),
          
     # ------ Path Clasificaciones ------ #

     path('lista_all_clasificaciones/',
          views.ClasificacionListView.as_view(),
          name='all_clasificaciones'),
     
     path('add-clasificacion',
          views.ClasificacionCreateView.as_view(),
          name='add_clasificacion'),

     path('delete-clasificacion/<pk>',
          views.ClasificacionDeleteView.as_view(),
          name='delete_clasificacion'),
     ]