from django.db import models
from django.db.models import Q

class EmpleadoManager(models.Manager):

    def buscar_empleado(self, kword):
        return self.filter(
            Q(first_name__icontains = kword) |
            Q(last_name__icontains = kword) |
            Q(id__icontains = kword)).order_by('id')

    def buscar_by_area(self, kword):
        return self.filter(
            departamento__name__icontains = kword
            ).order_by('id')

    def buscar_by_trabajo(self, kword):
        return self.filter(
            job__puesto__icontains = kword
            ).order_by('id')
    
class TrabajoManager(models.Manager):
    def buscar_trabajo(self, kword):
        return self.filter(
            Q(puesto__icontains = kword) |
            Q(id__icontains = kword)
        ).order_by('id')