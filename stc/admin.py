from django.contrib import admin

from .models import *


admin.site.register(Convenio)
admin.site.register(Empresa)
admin.site.register(Gestor)
admin.site.register(Causal)
admin.site.register(Unidad)
admin.site.register(Ejecutivo)
admin.site.register(Servicio)
admin.site.register(EstadoDV)
admin.site.register(Devolucion)
admin.site.register(Respuesta)
admin.site.register(EstadoGL)


class RadicacionAdmin(admin.ModelAdmin):
    list_display = (
        'factura',
        'convenio',
        'fecha_radicacion',
        'contrato_tipo',
        'valor_factura',
        'fecha_registro',
        )
admin.site.register(Radicacion, RadicacionAdmin)


class GlosaAdmin(admin.ModelAdmin):
    list_display = (
        'factura',
        'convenio',
        'valor_glosa',
        )
    search_fields = ['factura']
admin.site.register(Glosa, GlosaAdmin)
