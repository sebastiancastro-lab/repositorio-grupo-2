@admin.register(RegistroSigno)
class RegistroSignoAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'tipo_signo', 'dispositivo', 'valor_medido', 'fecha_hora', 'responsable')
    list_filter = ('tipo_signo', 'dispositivo')
