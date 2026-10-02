from django.db import models
from django.utils import timezone


class Paciente(models.Model):
    documento = models.CharField('Documento de Identidad', max_length=20, unique=True)
    nombres = models.CharField('Nombres', max_length=100)
    apellidos = models.CharField('Apellidos', max_length=100)
    edad = models.IntegerField('Edad')
    genero = models.CharField('Género', max_length=10)
    eps = models.CharField('EPS', max_length=100)

    class Meta:
        db_table = 'pacientes'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class TipoSigno(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    unidad_medida = models.CharField(max_length=20)
    valor_min_normal = models.FloatField()
    valor_max_normal = models.FloatField()

    class Meta:
        verbose_name = 'Tipo de Signo'
        verbose_name_plural = 'Tipos de Signo'

    def __str__(self):
        return self.nombre


class Dispositivo(models.Model):
    ESTADO_ACTIVO = 'activo'
    ESTADO_MANTENIMIENTO = 'en mantenimiento'
    ESTADO_FUERA_SERVICIO = 'fuera de servicio'
    ESTADOS = [
        (ESTADO_ACTIVO, 'Activo'),
        (ESTADO_MANTENIMIENTO, 'En mantenimiento'),
        (ESTADO_FUERA_SERVICIO, 'Fuera de servicio'),
    ]

    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=50, choices=ESTADOS)

    class Meta:
        verbose_name = 'Dispositivo'
        verbose_name_plural = 'Dispositivos'

    def __str__(self):
        return self.nombre


class RegistroSigno(models.Model):
    # PROTECT: no se puede borrar un paciente, tipo de signo o dispositivo
    # que ya tenga mediciones (evita perder historial clínico en cascada).
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='registros')
    tipo_signo = models.ForeignKey(TipoSigno, on_delete=models.PROTECT, related_name='registros')
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.PROTECT, related_name='registros')
    valor_medido = models.FloatField()
    fecha_hora = models.DateTimeField(default=timezone.now)
    responsable = models.CharField(max_length=100)

    class Meta:
        ordering = ['-fecha_hora', '-id']
        verbose_name = 'Registro de Signo'
        verbose_name_plural = 'Registros de Signos'

    def __str__(self):
        return f"{self.paciente} - {self.tipo_signo}: {self.valor_medido}"