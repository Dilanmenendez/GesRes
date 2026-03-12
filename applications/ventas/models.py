from django.db import models, transaction
from django.db.models import Sum
from .managers import VentaManager, PlatoManager
# Create your models here.

# --------- Plato Model ------------ #

class Plato(models.Model):

    nombre = models.CharField(max_length=120)

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    activo = models.BooleanField(default=True)

    objects = PlatoManager()

    def __str__(self):
        return self.nombre

# -------- IngredientePlato Model ----------- #

class IngredientePlato(models.Model):

    plato = models.ForeignKey(
        Plato,
        on_delete=models.CASCADE,
        related_name="ingredientes"
    )

    producto = models.ForeignKey(
        'stock.producto',
        on_delete=models.CASCADE
    )

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.producto} - {self.plato}"

# ---------- Venta Model ----------- #

class Venta(models.Model):

    fecha = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    objects = VentaManager()

    def __str__(self):
        return f"Venta {self.id}"

# ------ DetallesVenta Model ------------ #

class DetalleVenta(models.Model):

    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    plato = models.ForeignKey(
        Plato,
        on_delete=models.CASCADE
    )

    cantidad = models.PositiveIntegerField()

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        with transaction.atomic():
            nuevo = self.pk is None

            # Cálculo previo (Obligatorio antes de guardar)
            if not self.precio:
                self.precio = self.plato.precio
            
            self.cantidad = self.cantidad or 1
            self.subtotal = self.cantidad * self.precio

            # Primer guardado: Aquí el detalle ya tiene ID y subtotal
            super().save(*args, **kwargs)

            # Logica stock
            if nuevo:
                # Usamos select_for_update() para bloquear la fila del producto 
                # y que nadie más la toque hasta que terminemos
                for ingrediente in self.plato.ingredientes.select_related("producto"):
                    producto = ingrediente.producto
                    consumo = ingrediente.cantidad * self.cantidad
                    
                    producto.stock_actual -= consumo
                    producto.save(update_fields=["stock_actual"])

            # 4. Actualizar el total de la Venta 
            # Usamos filter().aggregate() para que la DB haga el trabajo pesado
            total_venta = self.venta.detalles.aggregate(
                res=Sum("subtotal")
            )["res"] or 0
            
            # Actualizamos la venta sin disparar toda la lógica pesada de Venta.save()
            self.venta.total = total_venta
            self.venta.save(update_fields=["total"])