from .models import Clasificacion

def clasificaciones_menu(request):
    return {
        "clasificaciones_menu": Clasificacion.objects.all()
    }