from django.urls import path
from . import views

urlpatterns = [
    path('hoome/', views.IndexView.as_view()), 
    #siempre que queramos mostrar un template en urls, debemos ponerle el .as_view()
    path('lista/', views.PruebaListView.as_view()),
    path('lista-prueba', views.ModeloPruebaListView.as_view()),
    path('add/',views.PruebaCreateView.as_view(), name='prueba_add'),
    path('prueba/', views.PruebaView.as_view(), name='prueba'),
    path('resume-foundation/', views.ResumeFoundationView.as_view(), name='resumen_foundation'),
]
