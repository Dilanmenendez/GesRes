from django.db import models
from django.db.models import Sum
from django.utils.timezone import now


# --------------- Venta Manager --------------- #

class VentaManager(models.Manager):

    def ventas_legitimas(self):
        return self.filter(
            anulada=False
        )
    
    def buscar_venta_id(self, venta_id):
        return self.filter(
            id=venta_id,
            anulada=False
        ).order_by('-id')

    def buscar_venta_fecha(self, fecha_venta):
        return self.filter(
            fecha__date=fecha_venta,
            anulada=False
        ).order_by('-fecha')


# --------------- Plato Manager --------------- #

class PlatoManager(models.Manager):

    def buscar_plato_kword(self, kword):
        return self.filter(
            nombre__icontains=kword
        ).order_by('nombre')

    def buscar_plato_id(self, id_plato):
        return self.filter(
            id=id_plato
        )

    def platos_activos(self):
        return self.filter(
            activo=True
        ).order_by('nombre')

