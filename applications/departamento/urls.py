from django.urls import path
from . import views


app_name = 'departamento_app'
urlpatterns = [
    path('list-all-departamentos', 
         views.DepartamentoListAllView.as_view(), 
         name='all_departamentos'),
    path('create-departamento/', 
         views.DepartamentoCreateView.as_view(), 
         name='create-departamento'),
    path('eliminar-departamento/<pk>', 
         views.DepartamentoDeleteView.as_view(), 
         name='delete-departamento'),
    path('update-empleado/<pk>', 
         views.DepartamentoUpdateView.as_view(), 
         name='departamento-update'),
]