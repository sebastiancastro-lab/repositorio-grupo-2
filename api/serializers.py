from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import Paciente, TipoSigno, Dispositivo, RegistroSigno


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id', 'documento', 'nombres', 'apellidos', 'edad', 'genero', 'eps']


class TipoSignoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSigno
        fields = '__all__'

    def validate(self, data):
        valor_min = data.get('valor_min_normal', getattr(self.instance, 'valor_min_normal', None))
        valor_max = data.get('valor_max_normal', getattr(self.instance, 'valor_max_normal', None))

        if valor_min is not None and valor_max is not None and valor_min >= valor_max:
            raise serializers.ValidationError(
                "valor_min_normal debe ser menor que valor_max_normal."
            )
        return data


class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = '__all__'
        extra_kwargs = {
            'numero_serie': {
                'error_messages': {'unique': 'Ya existe un dispositivo con ese número de serie.'}
            },
        }


class RegistroSignoSerializer(serializers.ModelSerializer):
    # Relaciones anidadas (solo lectura): la respuesta muestra el detalle, no solo el id.
    paciente_detalle = PacienteSerializer(source='paciente', read_only=True)
    tipo_signo_detalle = TipoSignoSerializer(source='tipo_signo', read_only=True)
    dispositivo_detalle = DispositivoSerializer(source='dispositivo', read_only=True)
    # Campo calculado: compara el valor con el rango normal del tipo de signo.
    estado_valor = serializers.SerializerMethodField()

    class Meta:
        model = RegistroSigno
        fields = [
            'id',
            'paciente', 'paciente_detalle',
            'tipo_signo', 'tipo_signo_detalle',
            'dispositivo', 'dispositivo_detalle',
            'valor_medido', 'estado_valor',
            'fecha_hora', 'responsable',
        ]

    def get_estado_valor(self, obj):
        tipo = obj.tipo_signo
        if obj.valor_medido < tipo.valor_min_normal:
            return 'bajo'
        if obj.valor_medido > tipo.valor_max_normal:
            return 'alto'
        return 'normal'

    def validate_valor_medido(self, value):
        if value < 0:
            raise serializers.ValidationError("El valor medido no puede ser negativo.")
        return value

    def validate_fecha_hora(self, value):
        # Margen de 5 minutos por diferencias de reloj entre cliente y servidor.
        if value > timezone.now() + timedelta(minutes=5):
            raise serializers.ValidationError("La fecha y hora no puede estar en el futuro.")
        return value

    def validate(self, data):
        dispositivo = data.get('dispositivo')
        # Solo se exige dispositivo activo al crear o al cambiarlo; así se puede
        # corregir un registro antiguo aunque su dispositivo ya esté fuera de servicio.
        cambia_dispositivo = (
            dispositivo is not None
            and (self.instance is None or dispositivo != self.instance.dispositivo)
        )
        if cambia_dispositivo and dispositivo.estado != Dispositivo.ESTADO_ACTIVO:
            raise serializers.ValidationError({
                'dispositivo': "No se puede registrar un signo con un dispositivo que no está activo."
            })
        return data