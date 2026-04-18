from decimal import Decimal

from django.test import TestCase

from applications.stock.models import Producto
from .models import DetalleVenta, IngredientePlato, Plato, Venta


class VentasModelsTest(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(tipo="MP", nombre="Queso", precio=Decimal("5.00"), stock_actual=Decimal("10.00"))
        self.plato = Plato.objects.create(nombre="Pizza", precio=Decimal("50.00"))
        IngredientePlato.objects.create(plato=self.plato, producto=self.producto, cantidad=Decimal("2.00"))

    def test_detalle_venta_actualiza_total_y_consumo_stock(self):
        venta = Venta.objects.create()
        DetalleVenta.objects.create(venta=venta, plato=self.plato, cantidad=2, precio=self.plato.precio, subtotal=Decimal("0.00"))
        venta.refresh_from_db()
        self.producto.refresh_from_db()

        self.assertEqual(venta.total, Decimal("100.00"))
        self.assertEqual(self.producto.stock_actual, Decimal("6.00"))

    def test_anular_venta_restaura_stock_y_total(self):
        venta = Venta.objects.create()
        DetalleVenta.objects.create(venta=venta, plato=self.plato, cantidad=2, precio=self.plato.precio, subtotal=Decimal("0.00"))
        venta.anular_venta()
        self.producto.refresh_from_db()
        venta.refresh_from_db()

        self.assertTrue(venta.anulada)
        self.assertEqual(venta.total, Decimal("0.00"))
        self.assertEqual(self.producto.stock_actual, Decimal("10.00"))
