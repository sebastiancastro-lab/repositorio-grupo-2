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

class RegistroSigno(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='registros')
    tipo_signo = models.ForeignKey('TipoSigno', on_delete=models.CASCADE)
    dispositivo = models.ForeignKey('Dispositivo', on_delete=models.CASCADE)
    valor_medido = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    responsable = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.paciente.documento} - {self.tipo_signo}: {self.valor_medido}"
