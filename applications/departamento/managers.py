from django.db import models
from django.db.models import Q

class DepartamentoManager(models.Manager):
    
    def buscar_departamento(self, kword):
        if kword == 'des':
            return self.filter().order_by('-id')
        
        return self.filter(
            Q(name__icontains = kword) |
            Q(short_name__icontains = kword)
            ).order_by('id')
    
    def buscar_departamento_id(self, id):
        return self.filter(
            id__icontains = id
        ).order_by('id')