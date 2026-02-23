from django.db import models
from django.core.validators import MinValueValidator

from .managers import ProduccionManager, RecetaManager


# Create your models here.
# --------- Modelo Receta --------- #
class Receta(models.Model):
    producto_final = models.OneToOneField('stock.Producto',
                                        on_delete=models.CASCADE,
                                        limit_choices_to={'tipo': 'PT'},
                                        related_name='receta')

    cantidad_por_receta = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )
    objects = RecetaManager()
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.producto_final.nombre

# ---------- Modelo Ingredientes Receta --------- #

class IngredientesReceta(models.Model):
    receta = models.ForeignKey(Receta, 
                                on_delete=models.CASCADE,
                                related_name='ingredientes')
    
    producto = models.ForeignKey('stock.Producto', 
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'tipo': 'MP'},
                                 related_name='ingredientes_receta')
    
    cantidad = models.DecimalField(default=0, 
                                   decimal_places=2,
                                   max_digits=10,
                                   validators = [MinValueValidator(0)]
                                   )
    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad}'

# --------- Modelo Produccion --------- #
class Produccion(models.Model):
    producto = models.ForeignKey(
        'stock.Producto',
        on_delete=models.PROTECT,
        limit_choices_to={'tipo': 'PT'}
    )

    cantidad_producida = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    fecha = models.DateTimeField(auto_now_add=True)

    costo_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    objects = ProduccionManager()

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad_producida}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.costo_total = (
                self.producto.costo_calculado * self.cantidad_producida
            )

        super().save(*args, **kwargs)