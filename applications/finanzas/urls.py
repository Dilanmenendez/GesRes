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
    path('cuentas/',
         views.CuentaListView.as_view(),
         name='all_cuentas'),

    path('cuentas/crear/',
        views.CuentaCreateView.as_view(),
        name='create_cuenta'),

    path('cuentas/<int:pk>/',
        views.CuentaDetailView.as_view(),
        name='detail_cuenta'),

    path('cuentas/<int:pk>/editar/',
        views.CuentaUpdateView.as_view(),
        name='update_cuenta'),

    path('cuentas/<int:pk>/eliminar/',
        views.CuentaDeleteView.as_view(),
        name='delete_cuenta'),

    # --------- Paths CategoriaMovimiento ----------- #
    path('categorias/',
        views.CategoriaMovimientoListView.as_view(),
        name='all_categorias'),

    path('categorias/crear/',
        views.CategoriaMovimientoCreateView.as_view(),
        name='create_categoria'),

    # --------- Paths GastoRecurrente ----------- #
    path('gastos-recurrentes/',
        views.GastoRecurrenteListView.as_view(),
        name='all_gastos_recurrentes'),

    path('gastos-recurrentes/crear/',
        views.GastoRecurrenteCreateView.as_view(),
        name='create_gasto_recurrente'),

    path('gastos-recurrentes/<int:pk>/editar/',
        views.GastoRecurrenteUpdateView.as_view(),
        name='update_gasto_recurrente'),

    # --------- Paths MovimientoFinanciero ----------- #
    path('movimientos/',
        views.MovimientoFinancieroListView.as_view(),
        name='all_movimientos'),

    path('movimientos/crear/',
        views.MovimientoFinancieroCreateView.as_view(),
        name='create_movimiento'),

    path('movimientos/<int:pk>/',
        views.MovimientoFinancieroDetailView.as_view(),
        name='detail_movimiento'),

    path('movimientos/<int:pk>/anular/',
        views.MovimientoFinancieroAnularView.as_view(),
        name='anular_movimiento'),

    ]