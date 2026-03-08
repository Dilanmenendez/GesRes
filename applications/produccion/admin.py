from django.contrib import admin
from .models import Receta, IngredientesReceta, Produccion


# -------- Ingredientes dentro de Receta -------- #

class IngredientesRecetaInline(admin.TabularInline):
    model = IngredientesReceta
    extra = 1

# -------- Admin Receta -------- #

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):

    list_display = (
        "producto_final",
        "cantidad_por_receta",
        "costo_total",
    )

    inlines = [
        IngredientesRecetaInline
    ]


# -------- Admin Produccion -------- #

@admin.register(Produccion)
class ProduccionAdmin(admin.ModelAdmin):

    list_display = (
        "producto",
        "cantidad_producida",
        "costo_total",
        "fecha",
    )

    readonly_fields = (
        "costo_total",
        "fecha",
    )

    list_filter = (
        "producto",
        "fecha",
    )

    search_fields = (
        "producto__nombre",
    )