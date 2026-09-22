from django.contrib import admin
from .models import Paciente, TipoSigno, Dispositivo, RegistroSigno

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'documento', 'nombres', 'apellidos', 'eps')

@admin.register(TipoSigno)
class TipoSignoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'unidad_medida', 'valor_min_normal', 'valor_max_normal')
    search_fields = ('nombre',)

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'marca', 'modelo', 'numero_serie', 'estado')

@admin.register(RegistroSigno)
class RegistroSignoAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'tipo_signo', 'dispositivo', 'valor_medido', 'fecha_hora', 'responsable')
    list_filter = ('tipo_signo', 'dispositivo')