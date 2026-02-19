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

    # ----- Path Receta ----- #

        path('lista_all_receta/',
            views.RecetaListView.as_view(),
            name='all_receta'),

    # ----- Path Ingredientes Receta ----- #

        path('lista_all_ingredientes_receta/',
            views.IngredientesRecetaListView.as_view(),
            name='all_ingredientes_receta'),
            ]