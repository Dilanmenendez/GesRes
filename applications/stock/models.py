from decimal import Decimal

from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.forms import ValidationError
from .managers import ProductoManager, ClasificacionManager, ProveedorManager, CompraManager, ConsumoManager
# Create your models here.


#--------------- Clasificacion Model -----------------#
class Clasificacion(models.Model):
    nombre = models.CharField(max_length=50, 
                              unique=True)
    objects = ClasificacionManager()

    class Meta:
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
# --------------- Proveedor Model --------------- #

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

#---------------- Producto Model -------------------#

class Producto(models.Model):
    TIPO_CHOICES = (
        ('MP', 'Materia Prima'),
        ('PT', 'Producto Terminado'),
        ('SC', 'Sin Clasificar'),
    )
    tipo = models.CharField(max_length=2, 
                            choices=TIPO_CHOICES,
                            default='SC'
                            )
    nombre = models.CharField(max_length=50, 
                              unique=True)
    precio = models.DecimalField (max_digits=10, 
                                  decimal_places=2, 
                                  validators = [MinValueValidator(0)],
                                  default=0
                                  )
    proveedor = models.ForeignKey(Proveedor, 
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True)
    clasificacion = models.ForeignKey(Clasificacion, 
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True)
    stock_actual = models.DecimalField(default=0,
                                       decimal_places=2,
                                       max_digits=10,
                                       validators = [MinValueValidator(0)]
                                       )
    stock_minimo = models.DecimalField(default=0, 
                                       decimal_places=2,
                                       max_digits=10,
                                       help_text='cantidad minima antes de disparar alerta',
                                       validators = [MinValueValidator(0)]
                                       )
    descripcion = models.TextField(blank=True)
    objects = ProductoManager()
    
    @property
    def costo_calculado(self):
        if self.tipo != 'PT':
            return self.precio

        # Si no tiene receta todavía
        if not hasattr(self, 'receta'):
            return 0

        return sum(
            ingrediente.cantidad * ingrediente.producto.precio
            for ingrediente in self.receta.ingredientes.all()
        )

    #validacion para dar consistencia
    def clean(self):
        if self.tipo == 'PT' and self.precio != 0:
            raise ValidationError({
                'precio': 'Un Producto Terminado no debe tener precio manual.'
            })

        if self.tipo == 'MP' and self.precio <= 0:
            raise ValidationError({
                'precio': 'La Materia Prima debe tener un precio mayor a 0.'
            })

    class Meta:
        ordering = ['nombre']
        
    def __str__(self):
        return f'{self.nombre}'
    

# ---------------- Compra Model -------------------#

class Compra(models.Model):
    
    producto = models.ForeignKey(Producto,
                                 on_delete=models.PROTECT,
                                 limit_choices_to={'tipo': 'MP'},
                                 related_name='compras')
    
    cantidad = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
        ) 
    
    total_pagado = models.DecimalField(
        max_digits=10, 
        decimal_places=2)

    fecha = models.DateTimeField(auto_now_add=True)

    objects = CompraManager()

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0.')

    def save(self, *args, **kwargs):

        if not self.pk:
            with transaction.atomic():

                producto = Producto.objects.select_for_update().get(pk=self.producto.pk)

                self.total_pagado = producto.precio * self.cantidad

                producto.stock_actual += self.cantidad
                producto.save()

        super().save(*args, **kwargs)
    
    def anular(self):
        with transaction.atomic():
            producto = Producto.objects.select_for_update().get(pk=self.producto.pk)

            if self.cantidad > producto.stock_actual:
                raise ValidationError("Stock inconsistente.")

            producto.stock_actual -= self.cantidad
            producto.save()

            self.delete()
            
# ---------------- Consumo Model ------------------- #

class Consumo(models.Model):
    producto = models.ForeignKey(Producto,
                                 limit_choices_to={'tipo': 'PT'},
                                 on_delete=models.PROTECT,
                                 related_name='consumos')
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
)

    fecha = models.DateTimeField(auto_now_add=True)

    motivo = models.CharField(max_length=75,
                               blank=True,
                               help_text='Motivo del consumo, ej: venta, muestra, etc.'
                               )
    objects = ConsumoManager()
    
    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad}'

    # ------------- Metodo Clean ------------ #
    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0.')
    
    # ------------- Metodo Save ------------ #
    def save(self, *args, **kwargs):

        self.full_clean()

        if not self.pk:
            with transaction.atomic():
                
                # accedemos al prodcto y restamos stock.
                producto = Producto.objects.select_for_update().get(pk=self.producto.pk)

                if self.cantidad > producto.stock_actual:
                    raise ValidationError(
                        f"No hay stock suficiente. Stock actual: {producto.stock_actual}"
                    )

                producto.stock_actual -= self.cantidad
                producto.save()

        super().save(*args, **kwargs)
    
    # ------------- Metodo Anulate ------------ #
    def anular(self):
        with transaction.atomic():
            producto = Producto.objects.select_for_update().get(pk=self.producto.pk)

            producto.stock_actual += self.cantidad
            producto.save()

            self.delete()