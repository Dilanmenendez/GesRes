from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from applications.stock.models import Clasificacion, Compra, Consumo, Producto, Proveedor


class StockModelsTest(TestCase):
    def test_producto_mp_precio_cero_es_invalido(self):
        producto = Producto(tipo="MP", nombre="Azucar", precio=Decimal("0.00"))
        with self.assertRaises(ValidationError):
            producto.full_clean()

    def test_producto_pt_precio_no_cero_es_invalido(self):
        producto = Producto(tipo="PT", nombre="Pan", precio=Decimal("10.00"))
        with self.assertRaises(ValidationError):
            producto.full_clean()

    def test_compra_save_actualiza_stock_y_total(self):
        producto = Producto.objects.create(tipo="MP", nombre="Harina", precio=Decimal("4.00"), stock_actual=Decimal("0.00"))
        compra = Compra(producto=producto, cantidad=Decimal("3.00"), total_pagado=Decimal("0.00"))
        compra.save()
        producto.refresh_from_db()

        self.assertEqual(compra.total_pagado, Decimal("12.00"))
        self.assertEqual(producto.stock_actual, Decimal("3.00"))

    def test_compra_anular_restaura_stock_y_elimina_compra(self):
        producto = Producto.objects.create(tipo="MP", nombre="Sal", precio=Decimal("2.00"), stock_actual=Decimal("0.00"))
        compra = Compra.objects.create(producto=producto, cantidad=Decimal("2.00"), total_pagado=Decimal("0.00"))
        compra.anular()

        producto.refresh_from_db()
        self.assertEqual(producto.stock_actual, Decimal("0.00"))
        self.assertFalse(Compra.objects.filter(pk=compra.pk).exists())

    def test_consumo_save_y_anular_actualizan_stock(self):
        producto = Producto.objects.create(tipo="MP", nombre="Aceite", precio=Decimal("10.00"), stock_actual=Decimal("5.00"))
        consumo = Consumo(producto=producto, cantidad=Decimal("2.00"))
        consumo.save()
        producto.refresh_from_db()

        self.assertEqual(producto.stock_actual, Decimal("3.00"))

        consumo.anular()
        producto.refresh_from_db()
        self.assertEqual(producto.stock_actual, Decimal("5.00"))
        self.assertFalse(Consumo.objects.filter(pk=consumo.pk).exists())

    def test_clasificacion_y_proveedor_str(self):
        clasificacion = Clasificacion.objects.create(nombre="Bebidas")
        proveedor = Proveedor.objects.create(nombre="Proveedor A", num_contacto="123", email="a@a.com")

        self.assertEqual(str(clasificacion), "Bebidas")
        self.assertEqual(str(proveedor), "Proveedor A")
