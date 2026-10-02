import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


def normalizar_estados(apps, schema_editor):
    """Convierte los estados que permitía el frontend anterior a los del enunciado."""
    Dispositivo = apps.get_model('api', 'Dispositivo')
    equivalencias = {
        'disponible': 'activo',
        'en uso': 'activo',
        'mantenimiento': 'en mantenimiento',
        'inactivo': 'fuera de servicio',
    }
    validos = {'activo', 'en mantenimiento', 'fuera de servicio'}
    for disp in Dispositivo.objects.all():
        actual = (disp.estado or '').strip().lower()
        nuevo = actual if actual in validos else equivalencias.get(actual, 'fuera de servicio')
        if nuevo != disp.estado:
            disp.estado = nuevo
            disp.save(update_fields=['estado'])


def copiar_valor(apps, schema_editor):
    """Copia valor -> valor_medido (evita RENAME COLUMN, que MariaDB < 10.5 no soporta)."""
    RegistroSigno = apps.get_model('api', 'RegistroSigno')
    RegistroSigno.objects.update(valor_medido=models.F('valor'))


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_paciente_options_alter_tiposigno_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dispositivo',
            options={'verbose_name': 'Dispositivo', 'verbose_name_plural': 'Dispositivos'},
        ),
        migrations.AlterModelOptions(
            name='registrosigno',
            options={'ordering': ['-fecha_hora', '-id'], 'verbose_name': 'Registro de Signo', 'verbose_name_plural': 'Registros de Signos'},
        ),
        # Se conserva el dato existente: valor -> valor_medido (sin RENAME COLUMN)
        migrations.AddField(
            model_name='registrosigno',
            name='valor_medido',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.RunPython(copiar_valor, migrations.RunPython.noop),
        migrations.RemoveField(model_name='registrosigno', name='valor'),
        migrations.AddField(
            model_name='registrosigno',
            name='responsable',
            field=models.CharField(default='Sin especificar', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registrosigno',
            name='fecha_hora',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='registrosigno',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='registros', to='api.paciente'),
        ),
        migrations.AlterField(
            model_name='registrosigno',
            name='tipo_signo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='registros', to='api.tiposigno'),
        ),
        migrations.AlterField(
            model_name='registrosigno',
            name='dispositivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='registros', to='api.dispositivo'),
        ),
        migrations.RunPython(normalizar_estados, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='dispositivo',
            name='estado',
            field=models.CharField(
                choices=[('activo', 'Activo'), ('en mantenimiento', 'En mantenimiento'), ('fuera de servicio', 'Fuera de servicio')],
                max_length=50,
            ),
        ),
    ]