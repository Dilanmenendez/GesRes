from django.db import models
from django.core.validators import MinValueValidator
from .managers import ProductoManager, ClasificacionManager, ProveedorManager
# Create your models here.


#--------------- Modelos de Atributos para Producto ------------------#
class Clasificacion(models.Model):
    nombre = models.CharField(max_length=50, 
                              unique=True)
    objects = ClasificacionManager()

    class Meta:
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    num_contacto = models.CharField(max_length=20)  
    email = models.EmailField(max_length=254)
    activo = models.BooleanField(default=True)
    direccion = models.CharField(max_length=50, 
                                 blank=True)
    objects = ProveedorManager()

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

#---------------- Modelo de Producto -------------------#
class Producto(models.Model):
    nombre = models.CharField(max_length=50, 
                              unique=True)
    precio = models.DecimalField (max_digits=10, 
                                  decimal_places=2, 
                                  validators = [MinValueValidator(0)]
                                  )
    proveedor = models.ForeignKey(Proveedor, 
                                  on_delete=models.PROTECT)
    clasificacion = models.ForeignKey(Clasificacion, 
                                      on_delete=models.PROTECT)
    stock_actual = models.IntegerField(default=0,
                                       validators = [MinValueValidator(0)]
                                       )
    stock_minimo = models.IntegerField(default=0, 
                                       help_text='cantidad minima antes de disparar alerta',
                                       validators = [MinValueValidator(0)]
                                       )
    descripcion = models.TextField(blank=True)
    objects = ProductoManager()
    
    class Meta:
        ordering = ['nombre']
        
    def __str__(self):
        return f'{self.nombre}'