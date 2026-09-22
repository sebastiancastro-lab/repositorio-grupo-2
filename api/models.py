from django.db import models

class Paciente(models.Model):
    documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    edad = models.IntegerField()
    genero = models.CharField(max_length=10)
    eps = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class TipoSigno(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    unidad_medida = models.CharField(max_length=20)
    valor_min_normal = models.FloatField()
    valor_max_normal = models.FloatField()

    def __str__(self):
        return f"{self.nombre} ({self.unidad_medida})"

    class Meta:
        verbose_name = "Tipo de Signo"
        verbose_name_plural = "Tipos de Signo"

class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} ({self.numero_serie})"

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
