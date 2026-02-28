from django.db import models
from django.core.validators import MinValueValidator, ValidationError
from django.db import transaction
from django.db.models import F
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
    
    @property
    def costo_total(self):
        return sum(
            ingrediente.costo_total
            for ingrediente in self.ingredientes.select_related("producto")
        )
    
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
    @property
    def costo_total(self):
        return self.cantidad * self.producto.precio
    

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

    def save(self, *args, **kwargs):

        if self.pk:
            # Si ya existe, no recalculamos nada
            return super().save(*args, **kwargs)

        with transaction.atomic():

            receta = getattr(self.producto, 'receta', None)
            if not receta:
                raise ValidationError("El producto no tiene receta asociada.")

            if receta.cantidad_por_receta <= 0:
                raise ValidationError("La receta tiene cantidad_por_receta inválida.")

            factor = self.cantidad_producida / receta.cantidad_por_receta

            costo_total = 0

            # Bloqueamos ingredientes para evitar problemas concurrentes
            ingredientes = receta.ingredientes.select_related('producto').select_for_update()

            for item in ingredientes:

                mp = item.producto
                consumo = item.cantidad * factor

                if mp.stock_actual < consumo:
                    raise ValidationError(
                        f"Stock insuficiente de {mp.nombre}. "
                        f"Disponible: {mp.stock_actual}, Necesario: {consumo}"
                    )

                # Descontamos usando F() para seguridad
                mp.stock_actual = F('stock_actual') - consumo
                mp.save(update_fields=['stock_actual'])

                costo_total += consumo * mp.precio

            # Sumamos stock al producto terminado
            producto_pt = self.producto.__class__.objects.select_for_update().get(pk=self.producto.pk)
            producto_pt.stock_actual = F('stock_actual') + self.cantidad_producida
            producto_pt.save(update_fields=['stock_actual'])

            self.costo_total = costo_total

            super().save(*args, **kwargs)
            
    def anular(self):
        with transaction.atomic():
            
            # bloqueamos esta fila de la db para evitar ediciones mientras se anula la producción
            producto_pt = self.producto.__class__.objects.select_for_update().get(pk=self.producto.pk)

            receta = getattr(producto_pt, 'receta', None)
            if not receta:
                raise ValidationError("El producto no tiene receta asociada.")

            if receta.cantidad_por_receta <= 0:
                raise ValidationError("La receta tiene cantidad_por_receta inválida.")

            factor = self.cantidad_producida / receta.cantidad_por_receta

            if producto_pt.stock_actual < self.cantidad_producida:
                raise ValidationError(
                    "No se puede anular. Stock insuficiente del producto terminado."
                )

            # esto bloquea todas las materias primas de las receta mientras estes anulando
            # evita que alguien las compre, consuma, o modifique
            ingredientes = receta.ingredientes.select_related('producto').select_for_update()

            #accedemos a cada materia prima, y calculamos la cantidad total usada por cada una
            for item in ingredientes:
                mp = item.producto
                consumo = item.cantidad * factor

                mp.stock_actual = F('stock_actual') + consumo
                mp.save(update_fields=['stock_actual'])

            producto_pt.stock_actual = F('stock_actual') - self.cantidad_producida
            producto_pt.save(update_fields=['stock_actual'])

            self.delete()