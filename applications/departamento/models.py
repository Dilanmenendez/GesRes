from django.db import models
from .managers import DepartamentoManager
# Create your models here.
class Departamento(models.Model):
    name = models.CharField('Nombre', 
                            max_length=50, 
                            unique=True)
    short_name = models.CharField('Nombre corto', 
                                  max_length=20, 
                                  unique=True)
    #editable=False sirve para que no se pueda editar un valor incluso desde el panel de administrador, sirve mas de lo que parece,
                #Sobre todo si estas en un proyecto donde tenes que darle permisos a otras personas
    
    anulate = models.BooleanField('Anulado', default= False)
    objects = DepartamentoManager()
    
    class Meta:
        verbose_name = 'Mi Departamento'
        verbose_name_plural = 'Departamentos de la Empresa'
        ordering = ['-name']
        unique_together = ('name', 'short_name')
        
    def __str__(self):
        return f'{self.name}'