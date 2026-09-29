from django.db import models

class Paciente(models.Model):
    documento = models.BigIntegerField(unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    edad = models.IntegerField()
    genero = models.CharField(max_length=20)
    eps = models.CharField(max_length=100)

    class Meta:
        db_table = 'api_paciente'  # Coincide con la tabla real en phpMyAdmin

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class TipoSigno(models.Model):
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=20)
    valor_min_normal = models.FloatField()
    valor_max_normal = models.FloatField()

    class Meta:
        db_table = 'api_tiposigno'  # Coincide con la tabla real en phpMyAdmin

    def __str__(self):
        return self.nombre


class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)

    class Meta:
        db_table = 'api_dispositivo'  # Coincide con la tabla real en phpMyAdmin

    def __str__(self):
        return self.nombre


class RegistroSigno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo_signo = models.ForeignKey(TipoSigno, on_delete=models.CASCADE)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    valor = models.FloatField()
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'api_registrosigno'  # Coincide con la tabla real en phpMyAdmin

    def __str__(self):
        return f"{self.paciente} - {self.tipo_signo}: {self.valor}"