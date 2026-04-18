from django.contrib import admin
from django.urls import path
from . import views


app_name = 'finanzas_app'

urlpatterns = [
    # ---------- Path Varios -----------#
    path('success/',
         views.SuccessView.as_view(),
         name='success'),

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


     ]