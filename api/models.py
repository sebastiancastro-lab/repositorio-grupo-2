from django.db import models

class Paciente(models.Model):
    documento = models.CharField(max_length=20, unique=True, verbose_name="Documento de Identidad")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    edad = models.IntegerField(verbose_name="Edad")
    genero = models.CharField(max_length=10, verbose_name="Género")
    eps = models.CharField(max_length=100, verbose_name="EPS")

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        db_table = "pacientes"
        
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class TipoSigno(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    unidad_medida = models.CharField(max_length=20)
    valor_min_normal = models.FloatField()
    valor_max_normal = models.FloatField()

    def __str__(self):
        return self.nombre

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
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='registros')
    tipo_signo = models.ForeignKey(TipoSigno, on_delete=models.CASCADE, related_name='registros')
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='registros')
    valor = models.FloatField()
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_signo.nombre}: {self.valor} ({self.paciente.nombres})"
