from django.urls import path
from . import views

app_name = 'produccion_app'

urlpatterns = [
    # ---------- Path Varios -----------#
        path('', 
            views.inicioView.as_view(), 
            name='Inicio'),
            
            ]