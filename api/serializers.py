from rest_framework import serializers
from .models import Paciente, TipoSigno, Dispositivo, RegistroSigno

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        # fields = '__all__'
        fields = ['id', 'documento', 'nombres', 'apellidos', 'edad', 'genero', 'eps']

class TipoSignoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSigno
        fields = '__all__'

class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = '__all__' 


class RegistroSignoSerializer(serializers.ModelSerializer):
    # Relaciones anidadas para lectura completa (Read/GET)
    paciente_detalle = PacienteSerializer(source='paciente', read_only=True)
    tipo_signo_detalle = TipoSignoSerializer(source='tipo_signo', read_only=True)
    dispositivo_detalle = DispositivoSerializer(source='dispositivo', read_only=True)

    class Meta:
        model = RegistroSigno
        fields = '__all__'       
        
