from django.db import models
from django.db.models import Sum

# Create your models here.

# --------- Plato Model ------------ #
class Plato(models.Model):

    nombre = models.CharField(max_length=120)

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

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

    created_at = models.DateTimeField(auto_now_add=True)

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

        nuevo = self.pk is None

        if self.precio is None:
            self.precio = self.plato.precio

        if not self.cantidad:
            self.cantidad = 1

        self.subtotal = self.cantidad * self.precio

        super().save(*args, **kwargs)

        if nuevo:
            for ingrediente in self.plato.ingredientes.select_related("producto"):

                producto = ingrediente.producto

                consumo = ingrediente.cantidad * self.cantidad

                producto.stock_actual -= consumo
                producto.save(update_fields=["stock_actual"])

        total = self.venta.detalles.aggregate(
            total=Sum("subtotal")
        )["total"] or 0

        self.venta.total = total
        self.venta.save(update_fields=["total"])

    def __str__(self):
        return f"{self.plato} x {self.cantidad}"