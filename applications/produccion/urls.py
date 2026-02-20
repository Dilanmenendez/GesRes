from django.urls import path
from . import views

app_name = 'produccion_app'

urlpatterns = [
    # ---------- Path Varios -----------#

        path('', 
            views.inicioView.as_view(), 
            name='Inicio'),

    # ----- Path Producción ----- #

        path('lista_all_produccion/', 
            views.ProduccionListView.as_view(),
            name='all_produccion'),

        path('create_produccion/',
            views.ProduccionCreateView.as_view(),
            name='create_produccion'),

    # ----- Path Receta ----- #

        path('lista_all_receta/',
            views.RecetaListView.as_view(),
            name='all_receta'),
        
        path('create_receta/',
            views.RecetaCreateView.as_view(),
            name='create_receta'),

    # ----- Path Ingredientes Receta ----- #

        path('create_ingredientes_receta/',
            views.IngredientesRecetaCreateView.as_view(),
            name='create_ingredientes_receta'),
            ]
        