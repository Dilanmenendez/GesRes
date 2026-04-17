from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.db.models import Sum
from django.utils import timezone


class MovimientoFinancieroManager(models.Manager):
    @staticmethod
    def _month_start(fecha):
        return fecha.replace(day=1)

    @staticmethod
    def _month_delta(fecha, delta):
        month = fecha.month - 1 + delta
        year = fecha.year + month // 12
        month = month % 12 + 1
        return fecha.replace(year=year, month=month, day=1)

    def _periodo_ultimos_meses(self, meses, referencia=None):
        referencia = referencia or timezone.localdate()
        fecha_final = referencia
        fecha_inicio = self._month_delta(self._month_start(referencia), -(meses - 1))
        return fecha_inicio, fecha_final

    def ingresos_ultimos_meses(self, meses=3, referencia=None):
        fecha_inicio, fecha_final = self._periodo_ultimos_meses(meses, referencia)
        resultado = self.filter(
            tipo="I",
            fecha__date__gte=fecha_inicio,
            fecha__date__lte=fecha_final,
        ).aggregate(total=Sum("monto"))
        return resultado["total"] or Decimal("0.00")

    def gastos_ultimos_meses(self, meses=3, referencia=None):
        fecha_inicio, fecha_final = self._periodo_ultimos_meses(meses, referencia)
        resultado = self.filter(
            tipo="E",
            fecha__date__gte=fecha_inicio,
            fecha__date__lte=fecha_final,
        ).aggregate(total=Sum("monto"))
        return resultado["total"] or Decimal("0.00")

    def punto_equilibrio_aproximado(self, meses=3, referencia=None):
        gastos = self.gastos_ultimos_meses(meses, referencia)
        if meses <= 0:
            return Decimal("0.00")
        return (gastos / Decimal(meses)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def balance_ultimos_meses(self, meses=3, referencia=None):
        ingresos = self.ingresos_ultimos_meses(meses, referencia)
        gastos = self.gastos_ultimos_meses(meses, referencia)
        return (ingresos - gastos).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
