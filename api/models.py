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
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=20)
    valor_min_normal = models.FloatField()
    valor_max_normal = models.FloatField()

    def __str__(self):
        return self.nombre

class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} ({self.numero_serie})"

class RegistroSigno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo_signo = models.ForeignKey(TipoSigno, on_delete=models.CASCADE)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    valor_medido = models.FloatField()
    fecha_hora = models.DateTimeField()
    responsable = models.CharField(max_length=100)

    def __str__(self):
        return f"Registro {self.id} - Paciente: {self.paciente.documento}"
