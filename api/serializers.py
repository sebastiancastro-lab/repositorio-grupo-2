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
    class Meta:
        model = RegistroSigno
        fields = '__all__'