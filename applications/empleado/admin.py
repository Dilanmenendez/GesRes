from django.contrib import admin
from .models import Empleado, Habilidades, Trabajo

admin.site.register(Habilidades)
admin.site.register(Trabajo)

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'departamento',
        'job',
        'full_name',
        'id',
    )

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    
    #Para la barra buscadora
    search_fields = ('first_name',)
    #Coso de habilidades
    filter_horizontal = ('habilidades',)
    #Filtros laterales
    list_filter = ('job', 'departamento', 'habilidades',)

admin.site.register(Empleado, EmpleadoAdmin)