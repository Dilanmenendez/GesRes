from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from applications.produccion.models import IngredientesReceta, Produccion, Receta
from applications.stock.models import Compra, Producto
from applications.ventas.models import Venta
from applications.finanzas.models import CategoriaMovimiento, Cuenta, GastoRecurrente, MovimientoFinanciero


class FinanzasViewsTest(TestCase):
    def setUp(self):
        self.cuenta = Cuenta.objects.create(nombre="Caja principal", tipo="caja")
        self.categoria_ingreso = CategoriaMovimiento.objects.create(nombre="Ventas", tipo="I")
        self.categoria_egreso = CategoriaMovimiento.objects.create(nombre="Servicios", tipo="E")

    def test_dashboard_finanzas_muestra_resumen(self):
        MovimientoFinanciero.objects.create(
            cuenta=self.cuenta,
            categoria=self.categoria_ingreso,
            tipo="I",
            monto=Decimal("100.00"),
            descripcion="Venta de prueba",
        )
        MovimientoFinanciero.objects.create(
            cuenta=self.cuenta,
            categoria=self.categoria_egreso,
            tipo="E",
            monto=Decimal("40.00"),
            descripcion="Servicio",
        )

        response = self.client.get(reverse('finanzas_app:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_cuentas'], 1)
        self.assertEqual(response.context['saldo_total'], Decimal('60.00'))
        self.assertEqual(response.context['ingresos_mes'], Decimal('100.00'))
        self.assertEqual(response.context['egresos_mes'], Decimal('40.00'))


class FinanzasFlowTest(TestCase):
    def setUp(self):
        self.cuenta = Cuenta.objects.create(nombre="Caja principal", tipo="caja")
        self.categoria = CategoriaMovimiento.objects.create(nombre="Servicios", tipo="E")

    def test_categoria_detail_view_loads(self):
        response = self.client.get(reverse('finanzas_app:detail_categoria', args=[self.categoria.pk]))
        self.assertEqual(response.status_code, 200)

    def test_gasto_recurrente_detail_view_loads(self):
        gasto = GastoRecurrente.objects.create(
            nombre="Internet",
            cuenta=self.cuenta,
            categoria=self.categoria,
            monto_total=Decimal('120.00'),
            meses=6,
        )

        response = self.client.get(reverse('finanzas_app:detail_gasto_recurrente', args=[gasto.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Internet')

    def test_categoria_delete_view_loads(self):
        response = self.client.get(reverse('finanzas_app:delete_categoria', args=[self.categoria.pk]))

        self.assertEqual(response.status_code, 200)

    def test_gasto_recurrente_delete_view_loads(self):
        gasto = GastoRecurrente.objects.create(
            nombre="Internet",
            cuenta=self.cuenta,
            categoria=self.categoria,
            monto_total=Decimal('120.00'),
            meses=6,
        )

        response = self.client.get(reverse('finanzas_app:delete_gasto_recurrente', args=[gasto.pk]))

        self.assertEqual(response.status_code, 200)


class FinanzasModelsTest(TestCase):
    def setUp(self):
        self.cuenta = Cuenta.objects.create(nombre="Caja principal", tipo="caja")
        self.categoria_ingreso = CategoriaMovimiento.objects.create(nombre="Ventas", tipo="I")
        self.categoria_egreso = CategoriaMovimiento.objects.create(nombre="Costo de producción", tipo="E")

    def test_cuenta_saldo_calcula_ingresos_y_egresos(self):
        MovimientoFinanciero.objects.create(cuenta=self.cuenta, tipo="I", monto=Decimal("100.00"))
        MovimientoFinanciero.objects.create(cuenta=self.cuenta, tipo="E", monto=Decimal("40.00"))
        self.assertEqual(self.cuenta.saldo(), Decimal("60.00"))

    def test_movimiento_financiero_valida_categoria_y_tipo(self):
        movimiento = MovimientoFinanciero(
            cuenta=self.cuenta,
            categoria=self.categoria_egreso,
            tipo="I",
            monto=Decimal("10.00"),
        )
        with self.assertRaises(ValidationError):
            movimiento.full_clean()

    def test_crear_desde_origen_guarda_origen_y_monto(self):
        venta = Venta.objects.create(total=Decimal("50.00"), anulada=False)
        movimiento = MovimientoFinanciero.crear_desde_origen(
            origen=venta,
            tipo="I",
            cuenta=self.cuenta,
            categoria=self.categoria_ingreso,
            descripcion="Venta prueba",
            documento="V1",
            monto=Decimal("50.00"),
        )
        self.assertEqual(movimiento.origen, venta)
        self.assertEqual(movimiento.importe(), Decimal("50.00"))

    def test_signal_generates_movimiento_desde_venta(self):
        venta = Venta.objects.create(total=Decimal("80.00"), anulada=False)
        movimiento = MovimientoFinanciero.objects.filter(origen_content_type__model="venta", origen_object_id=venta.pk).first()
        self.assertIsNotNone(movimiento)
        self.assertEqual(movimiento.categoria.nombre, "Ventas")
        self.assertEqual(movimiento.tipo, "I")

    def test_signal_generates_movimiento_desde_compra(self):
        producto = Producto.objects.create(tipo="MP", nombre="Harina", precio=Decimal("10.00"), stock_actual=Decimal("0.00"))
        compra = Compra.objects.create(producto=producto, cantidad=Decimal("2.00"), total_pagado=Decimal("0.00"))
        movimiento = MovimientoFinanciero.objects.filter(origen_content_type__model="compra", origen_object_id=compra.pk).first()
        self.assertIsNotNone(movimiento)
        self.assertEqual(movimiento.categoria.nombre, "Compra de insumos")
        self.assertEqual(movimiento.tipo, "E")

    def test_signal_generates_movimiento_desde_produccion(self):
        materia_prima = Producto.objects.create(tipo="MP", nombre="Levadura", precio=Decimal("5.00"), stock_actual=Decimal("10.00"))
        producto_pt = Producto.objects.create(tipo="PT", nombre="Pan", precio=Decimal("0.00"), stock_actual=Decimal("0.00"))
        receta = Receta.objects.create(producto_final=producto_pt, cantidad_por_receta=Decimal("1.00"))
        IngredientesReceta.objects.create(receta=receta, producto=materia_prima, cantidad=Decimal("2.00"))
        produccion = Produccion.objects.create(producto=producto_pt, cantidad_producida=Decimal("3.00"), costo_total=Decimal("0.00"))
        movimiento = MovimientoFinanciero.objects.filter(origen_content_type__model="produccion", origen_object_id=produccion.pk).first()
        self.assertIsNotNone(movimiento)
        self.assertEqual(movimiento.categoria.nombre, "Costo de producción")
        self.assertEqual(movimiento.tipo, "E")

    def test_gasto_recurrente_generar_movimiento_mensual(self):
        categoria = CategoriaMovimiento.objects.create(nombre="Servicios", tipo="E")
        gasto = GastoRecurrente.objects.create(
            nombre="Internet",
            cuenta=self.cuenta,
            categoria=categoria,
            monto_total=Decimal("1200.00"),
            meses=12,
        )
        movimiento = gasto.generar_movimiento_mensual()
        self.assertIsNotNone(movimiento)
        self.assertEqual(movimiento.categoria, categoria)
        self.assertEqual(movimiento.monto, gasto.monto_mensual)
        self.assertIsNone(gasto.generar_movimiento_mensual())
