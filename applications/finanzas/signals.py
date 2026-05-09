from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cuenta, CategoriaMovimiento, MovimientoFinanciero
from applications.produccion.models import Produccion
from applications.ventas.models import Venta
from applications.stock.models import Compra


def _get_default_cuenta():
    return Cuenta.objects.filter(activo=True).first() or Cuenta.objects.first()


ORIGEN_A_CATEGORIA = {
    Venta: ("Ventas", "I"),
    Produccion: ("Costo de producción", "E"),
    Compra: ("Compra de insumos", "E"),
}


def _get_or_create_categoria(nombre, tipo):
    categoria, created = CategoriaMovimiento.objects.get_or_create(
        nombre=nombre,
        tipo=tipo,
        defaults={'descripcion': f'Categoría automática para {nombre}'}
    )
    return categoria


def _get_categoria_para_origen(origen):
    datos = ORIGEN_A_CATEGORIA.get(origen.__class__)
    if not datos:
        raise ValueError(f"No hay categoría configurada para el origen {origen.__class__.__name__}")
    nombre, tipo = datos
    return _get_or_create_categoria(nombre, tipo)


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

    categoria = _get_categoria_para_origen(instance)

    with transaction.atomic():
        MovimientoFinanciero.crear_desde_origen(
            origen=instance,
            tipo="I",
            cuenta=cuenta,
            categoria=categoria,
            descripcion=f"Venta #{instance.pk}",
            documento=str(instance.pk),
            monto=instance.total,
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

    categoria = _get_categoria_para_origen(instance)

    with transaction.atomic():
        MovimientoFinanciero.crear_desde_origen(
            origen=instance,
            tipo="E",
            cuenta=cuenta,
            categoria=categoria,
            descripcion=f"Producción #{instance.pk}",
            documento=str(instance.pk),
            monto=instance.costo_total,
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

    categoria = _get_categoria_para_origen(instance)

    with transaction.atomic():
        MovimientoFinanciero.crear_desde_origen(
            origen=instance,
            tipo="E",
            cuenta=cuenta,
            categoria=categoria,
            descripcion=f"Compra de stock: {instance.producto.nombre}",
            documento=f"C{instance.pk}",
            monto=instance.total_pagado,
        )
