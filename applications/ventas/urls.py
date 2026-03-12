from django.urls import path
from . import views

app_name = 'ventas_app'

urlpatterns = [
    # --------- Paths Varios ---------- #

    path('',
         views.InicioView.as_view(),
         name='Inicio'),
    
    path('success/',
         views.SuccessView.as_view(),
         name='success'),

    # ----- Venta paths -------- #

    path("all_ventas/",
         views.VentaListView.as_view(),
         name='all_ventas'),
    
    path('add_venta/',
         views.VentaCreateView.as_view(),
         name='add_venta'),

    # --------- Plato paths ----------- #
    
    path("all_platos/",
         views.PlatoListView.as_view(),
         name='all_platos'),
     
     path('add_plato/',
          views.PlatoCreateView.as_view(),
          name='add_plato')
]