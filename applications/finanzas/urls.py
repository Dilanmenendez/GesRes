from django.contrib import admin
from django.urls import path
from . import views


app_name = 'finanzas_app'

urlpatterns = [
    # ---------- Path Varios -----------#
    path('success/',
         views.SuccessView.as_view(),
         name='success'),

    path('',
         views.InicioView.as_view(),
         name='inicio'),

    # --------- Paths Cuenta ----------- #

    path('all_cuentas/',
         views.CuentaListView.as_view(),
         name='all_cuentas'),

    path('create_cuenta/',
        views.CuentaCreateView.as_view(),
        name='create_cuenta'),
    
    path('update_cuenta/<pk>/',
        views.CuentaUpdateView.as_view(),
        name='update_cuenta'),
    
    path('delete_cuenta/<pk>',
        views.CuentaDeleteView.as_view(),
        name='delete_cuenta'),
    
    path('detail_cuenta/<pk>/',
        views.CuentaDetailView.as_view(),
        name='detail_cuenta'),

    # --------- Paths CategoriaMovimiento ----------- #

    path('all_categorias/',
        views.CategoriaMovimientoListView.as_view(),
        name='all_categorias'),

    path('create_categoria/',
        views.CategoriaMovimientoCreateView.as_view(),
        name='create_categoria'),

    # --------- Paths GastoRecurrente ----------- #

    path('all_gastos_recurrentes/',
        views.GastoRecurrenteListView.as_view(),
        name='all_gastos_recurrentes'),

    path('create_gasto_recurrente/',
        views.GastoRecurrenteCreateView.as_view(),
        name='create_gasto_recurrente'),

    path('update_gasto_recurrente/<pk>/',
        views.GastoRecurrenteUpdateView.as_view(),
        name='update_gasto_recurrente'),

    # --------- Paths MovimientoFinanciero ----------- #

    path('all_movimientos/',
        views.MovimientoFinancieroListView.as_view(),
        name='all_movimientos'),

    path('detail_movimiento/<pk>/',
        views.MovimientoFinancieroDetailView.as_view(),
        name='detail_movimiento'),

    path('create_movimiento/',
        views.MovimientoFinancieroCreateView.as_view(),
        name='create_movimiento'),

    path('anular_movimiento/<pk>/',
        views.MovimientoFinancieroAnularView.as_view(),
        name='anular_movimiento'),

    ]