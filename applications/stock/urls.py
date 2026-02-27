from django.contrib import admin
from django.urls import path
from . import views


app_name = 'stock_app'

urlpatterns = [
    # ---------- Path Varios -----------#
     path('', 
          views.InicioView.as_view(), 
          name='Inicio'),

     path('success_url', 
          views.SuccessView.as_view(), 
          name='success'),
     
     path('dashboard/',
          views.StockDashboardView.as_view(),
          name='dashboard'),
     

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
     
     path('update-producto/<pk>/',
          views.ProductoUpdateView.as_view(),
          name='update_producto'),

     path('detail-producto/<pk>/',
          views.ProductoDetailView.as_view(),
          name='detail_producto'),

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
     
     path('update-proveedor/<pk>',
          views.ProveedorUpdateView.as_view(),
          name='update_proveedor'),
     
     path('detail-proveedor/<pk>',
          views.ProveedorDetailView.as_view(),
          name='detail_proveedor'),

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
     
     path('update-clasificacion/<pk>',
          views.ClasificacionUpdateView.as_view(),
          name='update_clasificacion'),
     
     # -------- Path Compra --------- #

     path('add-compra/<pk>/',
          views.CompraCreateView.as_view(),
          name='add_compra'),

     path('lista_all_compras/',
          views.CompraListView.as_view(),
          name='all_compras'),
     
     path('anulate-compra/<pk>/',
          views.CompraAnulateView.as_view(),
          name='anulate_compra'),
     
     path('detail-compra/<pk>/',
          views.CompraDetailView.as_view(),
          name='detail_compra'),

     # -------- Path Consumo --------- #

     path('add-consumo/<pk>/',
          views.ConsumoCreateView.as_view(),
          name='add_consumo'),
     
     path('lista_all_consumos/',
          views.ConsumoListView.as_view(),
          name='all_consumos'),
     ]