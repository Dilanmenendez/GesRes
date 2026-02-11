from django.db import models
from django.db.models import Q


#----------- Managers para Producto ----------------#
class ProductoManager(models.Manager):
    
    def buscar_producto_id(self, producto_id):
        return self.filter(
            id = producto_id
        ).order_by('id')
    
    def buscar_producto(self, kword):
        if kword == 'des':
            return self.filter().order_by('-id')
        return self.filter(
            nombre__icontains = kword
        ).order_by('id')
    
#---------- Managers para Provedor ------------#
class ProveedorManager(models.Manager):

    def buscar_proveedor_id(self, proveedor_id):
        return self.filter(
            id = proveedor_id
        ).order_by('id')

    def buscar_proveedor(self, kword):
        if kword == 'des':
            return self.filter().order_by('-id')
        return self.filter(
            nombre__icontains = kword
        ).order_by('id')


#----------- Managers para Clasificacion ------------#
class ClasificacionManager(models.Manager):

    def buscar_clasificacion_id(self, clasificacion_id):
        return self.filter(
            id = clasificacion_id
        ).order_by('id')
    
    def buscar_clasificacion(self, kword):
        if kword == 'des':
            return self.filter().order_by('-id')
        return self.filter(
            nombre__icontains = kword
        ).order_by('id')