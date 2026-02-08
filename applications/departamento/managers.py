from django.db import models
from django.db.models import Q

class DepartamentoManager(models.Manager):
    
    def buscar_departamento(self, kword):
        return self.filter(
            Q(name__icontains = kword) |
            Q(short_name__icontains = kword)
        ).order_by('id')