from django.contrib import admin
from .models import Clasificacion, Proveedor, Producto
# Register your models here.

admin.site.register(Clasificacion)
admin.site.register(Proveedor)

class StockAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'precio',
        'proveedor',
        'clasificacion',
        'stock_actual',
        'stock_minimo',
        'descripcion',
    )
    
    #Para la barra buscadora
    search_fields = ('nombre',)
    #Filtros laterales
    list_filter = ('clasificacion', 'proveedor',)

admin.site.register(Producto, StockAdmin)