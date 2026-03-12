from django.urls import path
from . import views

app_name = 'ventas_app'

urlpatterns = [
    # --------- Paths Varios ---------- #
    path('',
         views.InicioView.as_view(),
         name='Inicio'),
    
    # ----- Venta paths -------- #

    path("all_ventas/",
         views.VentaListView.as_view(),
         name='all_ventas'),
    
    # --------- Plato paths ----------- #
    
    path("all_platos/",
         views.PlatoListView.as_view(),
         name='all_platos'),
         
]