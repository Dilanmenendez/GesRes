from django.contrib import admin

from .models import Cuenta, CategoriaMovimiento, GastoRecurrente, MovimientoFinanciero


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "tipo",
        "moneda",
        "activo",
        "descripcion",
    )
    list_filter = ("tipo", "moneda", "activo")
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)


@admin.register(CategoriaMovimiento)
class CategoriaMovimientoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo")
    list_filter = ("tipo",)
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(GastoRecurrente)
class GastoRecurrenteAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "cuenta",
        "categoria",
        "monto_total",
        "meses",
        "activo",
        "fecha_inicio",
        "creado_en",
    )
    list_filter = ("cuenta", "categoria", "activo")
    search_fields = ("nombre", "descripcion")
    readonly_fields = ("monto_mensual", "creado_en")
    fieldsets = (
        (None, {
            "fields": (
                "nombre",
                "descripcion",
                "cuenta",
                "categoria",
                "monto_total",
                "meses",
                "fecha_inicio",
                "activo",
            )
        }),
        ("Información", {
            "fields": ("monto_mensual", "creado_en"),
        }),
    )


@admin.register(MovimientoFinanciero)
class MovimientoFinancieroAdmin(admin.ModelAdmin):
    list_display = (
        "tipo",
        "fecha",
        "cuenta",
        "categoria",
        "monto",
        "documento",
        "descripcion",
        "origen",
        "creado_por",
    )
    list_filter = ("tipo", "cuenta", "categoria", "fecha")
    search_fields = ("descripcion", "documento", "origen_object_id")
    readonly_fields = ("creado_en",)
    ordering = ("-fecha", "-id")
