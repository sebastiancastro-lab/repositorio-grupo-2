from django.utils import timezone
from .models import Paciente, TipoSigno, Dispositivo, RegistroSigno


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

    def test_crear_registro_valido(self):
        data = {
            "paciente": self.paciente.id,
            "tipo_signo": self.tipo_signo.id,
            "dispositivo": self.dispositivo_activo.id,
            "valor_medido": 95,
            "responsable": "Enfermera López"
        }
        response = self.client.post('/api/registros/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_registro_dispositivo_inactivo_rechazado(self):
        data = {
            "paciente": self.paciente.id,
            "tipo_signo": self.tipo_signo.id,
            "dispositivo": self.dispositivo_inactivo.id,
            "valor_medido": 95,
            "responsable": "Enfermera López"
        }
        response = self.client.post('/api/registros/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_eliminar_registro(self):
        response = self.client.delete(f'/api/registros/{self.registro.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RegistroSigno.objects.filter(id=self.registro.id).exists())
