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
     
     path('detail_venta/<pk>/', 
          views.VentaDetailView.as_view(), 
          name='detail_venta'),

    # --------- Plato paths ----------- #
    
    path("all_platos/",
         views.PlatoListView.as_view(),
         name='all_platos'),
     
     path('add_plato/',
          views.PlatoCreateView.as_view(),
          name='add_plato'),
     
     path('detail_plato/<pk>/',
          views.PlatoDetailView.as_view(),
          name='detail_plato'),

     path('update_plato/<pk>/', 
          views.PlatoUpdateView.as_view(), 
          name='update_plato'),

     # ----- IngredientesPlato Paths --------- #

     path('add_ingrediente_plato/<pk>/',
          views.IngredientePlatoCreateView.as_view(),
          name='create_ingrediente_plato'),
     
     path('update_ingrediente_plato/<pk>/',
          views.IngredientePlatoUpdateView.as_view(),
          name='update_ingrediente_plato'),
          
]