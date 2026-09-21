from django.contrib import admin
from .models import TipoSigno

@admin.register(TipoSigno)
class TipoSignoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'unidad_medida', 'valor_min_normal', 'valor_max_normal')
    search_fields = ('nombre',)