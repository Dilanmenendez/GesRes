from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cuenta, CategoriaMovimiento, MovimientoFinanciero
from applications.produccion.models import Produccion
from applications.ventas.models import Venta
from applications.stock.models import Compra


def _get_default_cuenta():
    return Cuenta.objects.filter(activo=True).first() or Cuenta.objects.first()


def _get_categoria_por_tipo(tipo):
    return CategoriaMovimiento.objects.filter(tipo=tipo).first()


def _movimiento_existente(origen):
    origen_ct = ContentType.objects.get_for_model(origen)
    return MovimientoFinanciero.objects.filter(
        origen_content_type=origen_ct,
        origen_object_id=origen.pk,
    ).exists()


@receiver(post_save, sender=Venta)
def crear_movimiento_desde_venta(sender, instance, created, **kwargs):
    if instance.anulada:
        return

    if _movimiento_existente(instance):
        return

    if instance.total is None or instance.total <= 0:
        return

    cuenta = _get_default_cuenta()
    if not cuenta:
        return

    categoria = _get_categoria_por_tipo("I")

    MovimientoFinanciero.crear_desde_origen(
        origen=instance,
        tipo="I",
        cuenta=cuenta,
        categoria=categoria,
        descripcion=f"Venta #{instance.pk}",
        documento=str(instance.pk),
    )


@receiver(post_save, sender=Produccion)
def crear_movimiento_desde_produccion(sender, instance, created, **kwargs):
    if not created:
        return

    if _movimiento_existente(instance):
        return

    cuenta = _get_default_cuenta()
    if not cuenta:
        return

    categoria = _get_categoria_por_tipo("E")

    MovimientoFinanciero.crear_desde_origen(
        origen=instance,
        tipo="E",
        cuenta=cuenta,
        categoria=categoria,
        descripcion=f"Producción #{instance.pk}",
        documento=str(instance.pk),
    )


@receiver(post_save, sender=Compra)
def crear_movimiento_desde_compra(sender, instance, created, **kwargs):
    if not created:
        return

    if _movimiento_existente(instance):
        return

    if instance.total_pagado is None or instance.total_pagado <= 0:
        return

    cuenta = _get_default_cuenta()
    if not cuenta:
        return

    categoria = _get_categoria_por_tipo("E")

    MovimientoFinanciero.crear_desde_origen(
        origen=instance,
        tipo="E",
        cuenta=cuenta,
        categoria=categoria,
        descripcion=f"Compra de stock: {instance.producto.nombre}",
        documento=f"C{instance.pk}",
    )
