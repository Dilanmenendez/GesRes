from django.urls import path
from . import views

app_name = 'produccion_app'

urlpatterns = [
    # ---------- Path Varios -----------#

        path('', 
            views.inicioView.as_view(), 
            name='Inicio'),

        path('success_url', 
            views.SuccessView.as_view(),
            name='success'),

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

        path('detail_receta/<pk>/',
             views.RecetaDetailView.as_view(),
             name='detail_receta'),

    # ----- Path Ingredientes Receta ----- #

        path('create_ingredientes_receta/<pk>',
            views.IngredientesRecetaCreateView.as_view(),
            name='create_ingredientes_receta'),
            ]
        