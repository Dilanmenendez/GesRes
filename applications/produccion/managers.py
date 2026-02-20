from django.db import models
from django.db.models import Q

#----------- Managers para Produccion ----------------#

class ProduccionManager(models.Manager):
    def buscar_produccion_id(self, produccion_id):
        return self.filter(
            id = produccion_id
        ).order_by('id')
    
    def buscar_produccion(self,kword):
        return self.filter(
            producto__nombre__icontains = kword
        ).order_by('id')

# ----------- Managers para Receta ------------#

class RecetaManager(models.Manager):
    def buscar_receta_id(self, receta_id):
        return self.filter(
            id = receta_id
        ).order_by('id')
    
    def buscar_receta(self, kword):
        return self.filter(
            producto_final__nombre__icontains = kword
        ).order_by('id')
    
# ----------- Managers para Ingredientes Receta ------------#

class IngredientesRecetaManager(models.Manager):
    def buscar_ingredientes_receta_id(self, ingredientes_receta_id):
        return self.filter(
            id = ingredientes_receta_id
        ).order_by('id')
    
    def buscar_ingredientes_receta(self, kword):
        return self.filter(
            producto__nombre__icontains = kword
        ).order_by('id')