from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from applications.stock.models import Producto, Proveedor
from applications.produccion.models import IngredientesReceta, Produccion, Receta


class ProduccionModelsTest(TestCase):
    def setUp(self):
        self.proveedor = Proveedor.objects.create(nombre="Proveedor X", num_contacto="123", email="x@x.com")
        self.mp = Producto.objects.create(tipo="MP", nombre="Leche", precio=Decimal("2.00"), stock_actual=Decimal("10.00"))
        self.pt = Producto.objects.create(tipo="PT", nombre="Yogur", precio=Decimal("0.00"), stock_actual=Decimal("0.00"))
        self.receta = Receta.objects.create(producto_final=self.pt, cantidad_por_receta=Decimal("1.00"))
        IngredientesReceta.objects.create(receta=self.receta, producto=self.mp, cantidad=Decimal("2.00"))

    def test_produccion_sin_receta_levanta_error(self):
        producto_sin_receta = Producto.objects.create(tipo="PT", nombre="Helado", precio=Decimal("0.00"), stock_actual=Decimal("0.00"))
        produccion = Produccion(producto=producto_sin_receta, cantidad_producida=Decimal("1.00"), costo_total=Decimal("0.00"))
        with self.assertRaises(ValidationError):
            produccion.save()

    def test_produccion_guarda_costo_y_actualiza_stock(self):
        produccion = Produccion.objects.create(producto=self.pt, cantidad_producida=Decimal("3.00"), costo_total=Decimal("0.00"))
        self.mp.refresh_from_db()
        self.pt.refresh_from_db()

        self.assertEqual(self.mp.stock_actual, Decimal("4.00"))
        self.assertEqual(self.pt.stock_actual, Decimal("3.00"))
        self.assertEqual(produccion.costo_total, Decimal("12.00"))

    def test_anular_produccion_restaura_stock_y_elimina_registro(self):
        produccion = Produccion.objects.create(producto=self.pt, cantidad_producida=Decimal("3.00"), costo_total=Decimal("0.00"))
        produccion.anular()
        self.mp.refresh_from_db()
        self.pt.refresh_from_db()

        self.assertEqual(self.mp.stock_actual, Decimal("10.00"))
        self.assertEqual(self.pt.stock_actual, Decimal("0.00"))
        self.assertFalse(Produccion.objects.filter(pk=produccion.pk).exists())
