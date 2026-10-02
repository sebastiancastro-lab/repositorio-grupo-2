from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Paciente, TipoSigno, Dispositivo, RegistroSigno


class TipoSignoTests(APITestCase):
    def setUp(self):
        self.tipo = TipoSigno.objects.create(
            nombre="Frecuencia Cardíaca",
            unidad_medida="lpm",
            valor_min_normal=60,
            valor_max_normal=100
        )

    def test_listar_tipos_signo(self):
        response = self.client.get('/api/tipos-signo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_crear_tipo_signo_valido(self):
        data = {
            "nombre": "Temperatura Corporal",
            "unidad_medida": "°C",
            "valor_min_normal": 36.0,
            "valor_max_normal": 37.5
        }
        response = self.client.post('/api/tipos-signo/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_tipo_signo_rango_invalido(self):
        data = {
            "nombre": "Signo Inválido",
            "unidad_medida": "x",
            "valor_min_normal": 100,
            "valor_max_normal": 50
        }
        response = self.client.post('/api/tipos-signo/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_tipo_signo_nombre_duplicado(self):
        data = {
            "nombre": "Frecuencia Cardíaca",
            "unidad_medida": "lpm",
            "valor_min_normal": 60,
            "valor_max_normal": 100
        }
        response = self.client.post('/api/tipos-signo/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_actualizar_tipo_signo(self):
        response = self.client.patch(f'/api/tipos-signo/{self.tipo.id}/', {"valor_max_normal": 110})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tipo.refresh_from_db()
        self.assertEqual(self.tipo.valor_max_normal, 110)

    def test_eliminar_tipo_signo(self):
        response = self.client.delete(f'/api/tipos-signo/{self.tipo.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TipoSigno.objects.filter(id=self.tipo.id).exists())


class DispositivoTests(APITestCase):
    def setUp(self):
        self.dispositivo = Dispositivo.objects.create(
            nombre="Monitor A", marca="Philips", modelo="X1",
            numero_serie="SN001", estado="activo"
        )

    def _datos(self, **extra):
        datos = {
            "nombre": "Oxímetro", "marca": "Masimo", "modelo": "Rad-5",
            "numero_serie": "SN999", "estado": "activo",
        }
        datos.update(extra)
        return datos

    def test_listar_dispositivos(self):
        response = self.client.get('/api/dispositivos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_detalle_dispositivo(self):
        response = self.client.get(f'/api/dispositivos/{self.dispositivo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['numero_serie'], "SN001")

    def test_crear_dispositivo_valido(self):
        response = self.client.post('/api/dispositivos/', self._datos())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_dispositivo_numero_serie_duplicado(self):
        response = self.client.post('/api/dispositivos/', self._datos(numero_serie="SN001"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('numero_serie', response.data)

    def test_crear_dispositivo_estado_invalido(self):
        response = self.client.post('/api/dispositivos/', self._datos(estado="Disponible"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('estado', response.data)

    def test_crear_dispositivo_sin_estado(self):
        datos = self._datos()
        datos.pop('estado')
        response = self.client.post('/api/dispositivos/', datos)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_actualizar_estado(self):
        response = self.client.patch(
            f'/api/dispositivos/{self.dispositivo.id}/', {"estado": "en mantenimiento"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dispositivo.refresh_from_db()
        self.assertEqual(self.dispositivo.estado, "en mantenimiento")

    def test_filtrar_por_estado(self):
        Dispositivo.objects.create(
            nombre="Monitor B", marca="Philips", modelo="X2",
            numero_serie="SN002", estado="fuera de servicio"
        )
        response = self.client.get('/api/dispositivos/?estado=activo')
        self.assertEqual(len(response.data), 1)

    def test_eliminar_dispositivo(self):
        response = self.client.delete(f'/api/dispositivos/{self.dispositivo.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Dispositivo.objects.filter(id=self.dispositivo.id).exists())


class RegistroSignoTests(APITestCase):
    def setUp(self):
        self.paciente = Paciente.objects.create(
            documento="123456", nombres="Ana", apellidos="Gómez",
            edad=30, genero="F", eps="Sura"
        )
        self.tipo_signo = TipoSigno.objects.create(
            nombre="Frecuencia Cardíaca", unidad_medida="lpm",
            valor_min_normal=60, valor_max_normal=100
        )
        self.dispositivo_activo = Dispositivo.objects.create(
            nombre="Monitor A", marca="Philips", modelo="X1",
            numero_serie="SN001", estado="activo"
        )
        self.dispositivo_inactivo = Dispositivo.objects.create(
            nombre="Monitor B", marca="Philips", modelo="X2",
            numero_serie="SN002", estado="fuera de servicio"
        )
        self.registro = RegistroSigno.objects.create(
            paciente=self.paciente, tipo_signo=self.tipo_signo,
            dispositivo=self.dispositivo_activo, valor_medido=80,
            responsable="Enfermera López"
        )

    def _datos(self, **extra):
        datos = {
            "paciente": self.paciente.id,
            "tipo_signo": self.tipo_signo.id,
            "dispositivo": self.dispositivo_activo.id,
            "valor_medido": 95,
            "responsable": "Enfermera López",
        }
        datos.update(extra)
        return datos

    def test_listar_registros(self):
        response = self.client.get('/api/registros/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_respuesta_incluye_relaciones_anidadas(self):
        response = self.client.get(f'/api/registros/{self.registro.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['paciente_detalle']['documento'], "123456")
        self.assertEqual(response.data['tipo_signo_detalle']['nombre'], "Frecuencia Cardíaca")
        self.assertEqual(response.data['dispositivo_detalle']['numero_serie'], "SN001")

    def test_respuesta_incluye_campos_del_enunciado(self):
        response = self.client.get(f'/api/registros/{self.registro.id}/')
        for campo in ('id', 'paciente', 'tipo_signo', 'dispositivo',
                      'valor_medido', 'fecha_hora', 'responsable'):
            self.assertIn(campo, response.data)

    def test_crear_registro_valido(self):
        response = self.client.post('/api/registros/', self._datos())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['fecha_hora'])  # se asigna sola si no se envía

    def test_crear_registro_dispositivo_inactivo_rechazado(self):
        response = self.client.post(
            '/api/registros/', self._datos(dispositivo=self.dispositivo_inactivo.id)
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dispositivo', response.data)

    def test_crear_registro_valor_negativo_rechazado(self):
        response = self.client.post('/api/registros/', self._datos(valor_medido=-5))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_registro_fecha_futura_rechazada(self):
        futura = (timezone.now() + timedelta(days=1)).isoformat()
        response = self.client.post('/api/registros/', self._datos(fecha_hora=futura))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_registro_sin_responsable_rechazado(self):
        datos = self._datos()
        datos.pop('responsable')
        response = self.client.post('/api/registros/', datos)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_estado_valor_normal_alto_bajo(self):
        normal = self.client.get(f'/api/registros/{self.registro.id}/').data
        self.assertEqual(normal['estado_valor'], 'normal')
        alto = self.client.post('/api/registros/', self._datos(valor_medido=130)).data
        self.assertEqual(alto['estado_valor'], 'alto')
        bajo = self.client.post('/api/registros/', self._datos(valor_medido=40)).data
        self.assertEqual(bajo['estado_valor'], 'bajo')

    def test_editar_registro_antiguo_con_dispositivo_ya_inactivo(self):
        # El dispositivo se da de baja después de tomar la medición: aún se puede corregir el registro.
        self.dispositivo_activo.estado = "fuera de servicio"
        self.dispositivo_activo.save()
        response = self.client.patch(
            f'/api/registros/{self.registro.id}/', {"responsable": "Dr. Pérez"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cambiar_a_dispositivo_inactivo_rechazado(self):
        response = self.client.patch(
            f'/api/registros/{self.registro.id}/', {"dispositivo": self.dispositivo_inactivo.id}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filtrar_por_paciente(self):
        otro = Paciente.objects.create(
            documento="999", nombres="Luis", apellidos="Mora", edad=50, genero="M", eps="Sanitas"
        )
        self.client.post('/api/registros/', self._datos(paciente=otro.id))
        response = self.client.get(f'/api/registros/?paciente={otro.id}')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['paciente'], otro.id)

    def test_eliminar_registro(self):
        response = self.client.delete(f'/api/registros/{self.registro.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RegistroSigno.objects.filter(id=self.registro.id).exists())

    def test_no_se_elimina_dispositivo_con_registros(self):
        response = self.client.delete(f'/api/dispositivos/{self.dispositivo_activo.id}/')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertTrue(Dispositivo.objects.filter(id=self.dispositivo_activo.id).exists())

    def test_no_se_elimina_tipo_signo_con_registros(self):
        response = self.client.delete(f'/api/tipos-signo/{self.tipo_signo.id}/')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class DatosInicialesTests(APITestCase):
    """Garantiza que la BD precargada cumple el mínimo del enunciado."""
    fixtures = ['datos_iniciales']

    def test_minimos_precargados(self):
        self.assertGreaterEqual(Paciente.objects.count(), 5)
        self.assertGreaterEqual(TipoSigno.objects.count(), 4)
        self.assertGreaterEqual(Dispositivo.objects.count(), 3)
        self.assertGreaterEqual(RegistroSigno.objects.count(), 5)

    def test_get_no_devuelve_listas_vacias(self):
        for ruta in ('pacientes', 'tipos-signo', 'dispositivos', 'registros'):
            response = self.client.get(f'/api/{ruta}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertGreater(len(response.data), 0, ruta)