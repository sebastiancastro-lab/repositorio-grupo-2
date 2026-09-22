from rest_framework.test import APITestCase
from rest_framework import status
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
