from django.db import models, transaction
from django.db.models import Sum
from .managers import VentaManager, PlatoManager
from applications.stock.models import Consumo
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
            
            # 1. Cálculos de precio y subtotal del detalle
            if not self.precio:
                self.precio = self.plato.precio
            self.cantidad = self.cantidad or 1
            self.subtotal = self.cantidad * self.precio

            # 2. Guardamos el detalle primero para tener ID
            super().save(*args, **kwargs)

            if nuevo:
                for ingrediente in self.plato.ingredientes.select_related("producto"):
                    # (Cantidad que pide la receta) x (Cantidad de platos vendidos)
                    cantidad_total_consumo = ingrediente.cantidad * self.cantidad

                    # Esto descuenta el stock_actual del Producto (sea MP o PT)
                    Consumo.objects.create(
                        producto=ingrediente.producto,
                        cantidad=cantidad_total_consumo,
                        motivo=f"Venta #{self.venta.id} - Plato: {self.plato.nombre}",
                    )

            # 3. Actualizar el total de la Venta
            total_venta = self.venta.detalles.aggregate(
                res=Sum("subtotal")
            )["res"] or 0
            
            self.venta.total = total_venta
            self.venta.save(update_fields=["total"])