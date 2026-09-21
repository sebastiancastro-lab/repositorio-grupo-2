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

class RegistroSignoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroSigno
        fields = '__all__'