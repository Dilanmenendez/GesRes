from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

# ------ Views Varios --------- #
class inicioView(TemplateView):
    template_name = "produccion/inicio.html"