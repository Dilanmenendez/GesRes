from django.db import models
from django.db.models import Q

class EmpleadoManager(models.Manager):
    #Managers para listAllEmpleado
    def buscar_empleado(self, kword):
        if kword == 'des':
            return self.filter().order_by('-id')
        
        return self.filter(
            Q(first_name__icontains = kword) |
            Q(last_name__icontains = kword)).order_by('id')
    
    def buscar_empleado_id(self, id):
        return self.filter(
            id__icontains = id
        ).order_by('id')
    
    #Maagers para Filtrar por Puesto / Departamento
    def buscar_by_area(self, kword):
        return self.filter(
            departamento__name__icontains = kword
            ).order_by('id')

    def buscar_by_trabajo(self, kword):
        return self.filter(
            job__puesto__icontains = kword
            ).order_by('id')

# Managers para Trabajo
class TrabajoManager(models.Manager):
    def buscar_trabajo(self, kword):
        if kword == 'des':
            return self.filter().order_by('-id')
        
        return self.filter(
            Q(puesto__icontains = kword)
        ).order_by('id')
    
    def buscar_trabajo_id(self, id):
        return self.filter(
            id__icontains = id
        ).order_by('id')