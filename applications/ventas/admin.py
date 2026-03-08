from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Plato, IngredientePlato, Venta, DetalleVenta


# -------- Ingredientes dentro del Plato -------- #

class IngredientePlatoInline(admin.TabularInline):
    model = IngredientePlato
    extra = 1


# -------- Admin de Plato -------- #

@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "precio",
        "activo",
    )

    list_filter = (
        "activo",
    )

    search_fields = (
        "nombre",
    )

    inlines = [
        IngredientePlatoInline
    ]


# -------- Detalles dentro de la Venta -------- #

class DetalleVentaInline(admin.TabularInline):

    model = DetalleVenta
    extra = 1
    
    readonly_fields = [
        'subtotal',
        'precio'
    ]


# -------- Admin de Venta -------- #

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "fecha",
        "total",
    )

    readonly_fields = (
        "fecha",
        "total"
    )

    inlines = [
        DetalleVentaInline
    ]


# -------- Admin DetalleVenta (opcional) -------- #

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):

    list_display = (
        "venta",
        "plato",
        "cantidad",
        "precio",
        "subtotal",
    )

    list_filter = (
        "plato",
    )

    search_fields = (
        "plato__nombre",
    )