from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import Case, DecimalField, F, Sum, When
from django.db.models.functions import Coalesce
from django.utils import timezone

from .managers import MovimientoFinancieroManager


class Cuenta(models.Model):
    TIPO_CHOICES = [
        ("caja", "Caja"),
        ("banco", "Banco"),
        ("tarjeta", "Tarjeta"),
        ("otro", "Otro"),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default="caja")
    moneda = models.CharField(max_length=3, default="ARS")
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        return self.nombre

    def saldo(self):
        agregados = self.movimientofinanciero_set.aggregate(
            saldo=Sum(
                Case(
                    When(tipo="I", then=Coalesce(F("monto"), 0)),
                    When(tipo="E", then=Coalesce(F("monto"), 0) * -1),
                    output_field=DecimalField(),
                )
            )
        )
        return agregados["saldo"] or 0


class CategoriaMovimiento(models.Model):
    TIPO_CHOICES = [("I", "Ingreso"), ("E", "Egreso")]

    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoría de movimiento"
        verbose_name_plural = "Categorías de movimientos"

    def __str__(self):
        return self.nombre


class GastoRecurrente(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    categoria = models.ForeignKey(
        CategoriaMovimiento,
        on_delete=models.PROTECT,
        limit_choices_to={"tipo": "E"},
    )
    monto_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    meses = models.PositiveIntegerField(default=12, validators=[MinValueValidator(1)])
    fecha_inicio = models.DateField(default=timezone.localdate)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gasto recurrente"
        verbose_name_plural = "Gastos recurrentes"
        ordering = ["-fecha_inicio", "nombre"]

    def __str__(self):
        return self.nombre

    @property
    def monto_mensual(self):
        if self.monto_total is None or self.meses in (None, 0):
            return Decimal("0.00")
        return (self.monto_total / Decimal(self.meses)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    def movimiento_para_mes(self, fecha=None):
        fecha = fecha or timezone.localdate()
        origen_ct = ContentType.objects.get_for_model(self)
        return MovimientoFinanciero.objects.filter(
            origen_content_type=origen_ct,
            origen_object_id=self.pk,
            fecha__year=fecha.year,
            fecha__month=fecha.month,
        ).first()

    def generar_movimiento_mensual(self, fecha=None):
        if not self.activo:
            return None

        fecha = fecha or timezone.localdate()
        if self.movimiento_para_mes(fecha):
            return None

        return MovimientoFinanciero.crear_desde_origen(
            origen=self,
            tipo="E",
            cuenta=self.cuenta,
            categoria=self.categoria,
            descripcion=self.descripcion or f"Gasto recurrente {self.nombre}",
            documento=f"GR-{self.pk}-{fecha.year}{fecha.month:02}",
            fecha=timezone.datetime(
                fecha.year,
                fecha.month,
                min(fecha.day, 28),
            ),
            monto=self.monto_mensual,
        )


class MovimientoFinanciero(models.Model):
    TIPO_CHOICES = [("I", "Ingreso"), ("E", "Egreso")]

    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    categoria = models.ForeignKey(
        CategoriaMovimiento, on_delete=models.PROTECT, null=True, blank=True
    )
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    fecha = models.DateTimeField(default=timezone.now)
    monto = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    descripcion = models.CharField(max_length=255, blank=True)
    documento = models.CharField(max_length=100, blank=True)
    anulado = models.BooleanField(default=False)

    objects = MovimientoFinancieroManager()

    creado_en = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    origen_content_type = models.ForeignKey(
        ContentType, null=True, blank=True, on_delete=models.PROTECT
    )
    origen_object_id = models.PositiveIntegerField(null=True, blank=True)
    origen = GenericForeignKey("origen_content_type", "origen_object_id")

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name = "Movimiento financiero"
        verbose_name_plural = "Movimientos financieros"

    def __str__(self):
        return f"{self.get_tipo_display()} {self.importe()} - {self.cuenta}"

    def importe(self):
        if self.monto is not None:
            return self.monto
        return self._importe_origen() or 0

    def _importe_origen(self):
        if self.origen is None:
            return None
        for attr in ("monto", "total", "costo_total", "importe"):
            valor = getattr(self.origen, attr, None)
            if valor is not None:
                return valor
        return None

    def clean(self):
        if self.origen_content_type and not self.origen_object_id:
            raise ValidationError("Origen incompleto.")
        if self.origen_object_id and not self.origen_content_type:
            raise ValidationError("Origen incompleto.")
        if self.monto is None and self.origen is None:
            raise ValidationError("Debe indicar un monto o un origen válido.")
        if self.categoria and self.categoria.tipo != self.tipo:
            raise ValidationError("La categoría no coincide con el tipo de movimiento.")

    def save(self, *args, **kwargs):
        if self.monto is None and self.origen is not None:
            self.monto = self._importe_origen()
        if self.monto is not None:
            self.monto = self.monto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.full_clean()
        super().save(*args, **kwargs)

    def anular(self):
        if self.anulado:
            return

        with transaction.atomic():
            # Si existe un origen, anulamos el origen primero
            # Esto asegura que el stock se devuelva correctamente
            if self.origen:
                origen_class_name = self.origen.__class__.__name__
                
                # Venta devuelve ingredientes al stock
                if origen_class_name == 'Venta':
                    self.origen.anular_venta()
                # Producción devuelve ingredientes y resta producto terminado
                elif origen_class_name == 'Produccion':
                    self.origen.anular()
                # Compra devuelve el stock de materia prima
                elif origen_class_name == 'Compra':
                    self.origen.anular()
            
            # Finalmente marcamos el movimiento como anulado
            self.anulado = True
            self.save(update_fields=["anulado"])

    @classmethod
    def crear_desde_origen(
        cls,
        origen,
        tipo,
        cuenta,
        categoria=None,
        descripcion="",
        documento="",
        fecha=None,
        monto=None,
    ):
        origen_ct = ContentType.objects.get_for_model(origen)
        movimiento = cls(
            cuenta=cuenta,
            categoria=categoria,
            tipo=tipo,
            origen_content_type=origen_ct,
            origen_object_id=origen.pk,
            descripcion=descripcion,
            documento=documento,
        )
        if fecha is not None:
            movimiento.fecha = fecha
        if monto is not None:
            movimiento.monto = monto
        movimiento.save()
        return movimiento

