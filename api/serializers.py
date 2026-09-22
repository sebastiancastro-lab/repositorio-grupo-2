from rest_framework import serializers
from .models import Paciente, TipoSigno, Dispositivo, RegistroSigno

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class TipoSignoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSigno
        fields = '__all__'

class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = '__all__' 


class RegistroSignoSerializer(serializers.ModelSerializer):
    paciente_detalle = PacienteSerializer(source='paciente', read_only=True)
    tipo_signo_detalle = TipoSignoSerializer(source='tipo_signo', read_only=True)
    dispositivo_detalle = DispositivoSerializer(source='dispositivo', read_only=True)

    class Meta:
        model = RegistroSigno
        fields = '__all__'

    def validate(self, data):
        dispositivo = data.get('dispositivo', getattr(self.instance, 'dispositivo', None))
        if dispositivo and dispositivo.estado != 'activo':
            raise serializers.ValidationError(
                "No se puede registrar un signo con un dispositivo que no está activo."
            )
        return data
