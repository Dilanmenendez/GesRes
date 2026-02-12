from django.contrib import admin
from django.urls import path
from . import views


app_name = 'stock_app'

urlpatterns = [
    path('', 
         views.InicioView.as_view(), 
         name='Inicio'),
    path('lista_all_productos/', 
         views.ProductoListView.as_view(), 
         name='all_productos'),
    path('lista_all_proveedores/', 
         views.ProveedorListView.as_view(), 
         name='all_proveedores'),
    path('lista_all_clasificaciones/',
         views.ClasificacionListView.as_view(),
         name='all_clasificaciones'),
]