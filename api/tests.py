from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from .models import Paciente, TipoSigno, Dispositivo, RegistroSigno

class PacienteAPITestCase(APITestCase):

    def setUp(self):
        # Crear un paciente mock de prueba antes de cada test
        self.paciente_mock = Paciente.objects.create(
            documento="1234567890",
            nombres="Prueba",
            apellidos="Mock",
            edad=30,
            genero="Masculino",
            eps="Sura"
        )

    def test_listar_pacientes(self):
        """Probar que el GET /api/pacientes/ retorne lista con el mock"""
        response = self.client.get('/api/pacientes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_crear_paciente_mock(self):
        """Probar que el POST cree un nuevo paciente correctamente"""
        data = {
            "documento": "9998887776",
            "nombres": "Laura",
            "apellidos": "Gómez",
            "edad": 25,
            "genero": "Femenino",
            "eps": "Sanitas"
        }
        response = self.client.post('/api/pacientes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class PacienteAPITestCase2(APITestCase):

    def setUp(self):
        """Se ejecuta antes de cada test para preparar un paciente inicial en la base de datos de pruebas."""
        self.paciente_datos = {
            "documento": "1017000111",
            "nombres": "Carlos Alberto",
            "apellidos": "Pérez Gómez",
            "edad": 40,
            "genero": "Masculino",
            "eps": "Sura"
        }
        self.paciente = Paciente.objects.create(**self.paciente_datos)
        self.list_url = '/api/pacientes/'
        self.detail_url = f'/api/pacientes/{self.paciente.id}/'

    def test_listar_pacientes(self):
        """Probar obtención de lista de pacientes (GET /api/pacientes/)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_obtener_detalle_paciente(self):
        """Probar consulta de un paciente por ID (GET /api/pacientes/{id}/)"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['documento'], self.paciente.documento)

    def test_crear_paciente_exitoso(self):
        """Probar creación de un paciente con datos válidos (POST /api/pacientes/)"""
        nuevo_paciente = {
            "documento": "1020999888",
            "nombres": "María Fernanda",
            "apellidos": "Rodríguez",
            "edad": 28,
            "genero": "Femenino",
            "eps": "Sanitas"
        }
        response = self.client.post(self.list_url, nuevo_paciente, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Paciente.objects.count(), 2)

    def test_actualizar_paciente(self):
        """Probar actualización de datos de un paciente (PATCH /api/pacientes/{id}/)"""
        datos_actualizados = {"eps": "Nueva EPS"}
        response = self.client.patch(self.detail_url, datos_actualizados, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.paciente.refresh_from_db()
        self.assertEqual(self.paciente.eps, "Nueva EPS")

    def test_eliminar_paciente(self):
        """Probar eliminación de un paciente (DELETE /api/pacientes/{id}/)"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Paciente.objects.count(), 0)

    def test_documento_duplicado_falla(self):
        """Probar que no permite crear dos pacientes con el mismo documento (Validación unique)"""
        datos_duplicados = self.paciente_datos.copy()
        response = self.client.post(self.list_url, datos_duplicados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class RegistroSignoTests(APITestCase):
#     def setUp(self):
#         self.paciente = Paciente.objects.create(
#             documento="123456", nombres="Ana", apellidos="Gómez",
#             edad=30, genero="F", eps="Sura"
#         )
#         self.tipo_signo = TipoSigno.objects.create(
#             nombre="Frecuencia Cardíaca", unidad_medida="lpm",
#             valor_min_normal=60, valor_max_normal=100
#         )
#         self.dispositivo_activo = Dispositivo.objects.create(
#             nombre="Monitor A", marca="Philips", modelo="X1",
#             numero_serie="SN001", estado="activo"
#         )
#         self.dispositivo_inactivo = Dispositivo.objects.create(
#             nombre="Monitor B", marca="Philips", modelo="X2",
#             numero_serie="SN002", estado="fuera de servicio"
#         )
#         self.registro = RegistroSigno.objects.create(
#             paciente=self.paciente, tipo_signo=self.tipo_signo,
#             dispositivo=self.dispositivo_activo, valor_medido=80,
#             responsable="Enfermera López"
#         )

#     def test_listar_registros(self):
#         response = self.client.get('/api/registros/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#     def test_respuesta_incluye_relaciones_anidadas(self):
#         response = self.client.get(f'/api/registros/{self.registro.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['paciente_detalle']['documento'], "123456")
#         self.assertEqual(response.data['tipo_signo_detalle']['nombre'], "Frecuencia Cardíaca")
#         self.assertEqual(response.data['dispositivo_detalle']['numero_serie'], "SN001")

#     def test_crear_registro_valido(self):
#         data = {
#             "paciente": self.paciente.id,
#             "tipo_signo": self.tipo_signo.id,
#             "dispositivo": self.dispositivo_activo.id,
#             "valor_medido": 95,
#             "responsable": "Enfermera López"
#         }
#         response = self.client.post('/api/registros/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_crear_registro_dispositivo_inactivo_rechazado(self):
#         data = {
#             "paciente": self.paciente.id,
#             "tipo_signo": self.tipo_signo.id,
#             "dispositivo": self.dispositivo_inactivo.id,
#             "valor_medido": 95,
#             "responsable": "Enfermera López"
#         }
#         response = self.client.post('/api/registros/', data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_eliminar_registro(self):
#         response = self.client.delete(f'/api/registros/{self.registro.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(RegistroSigno.objects.filter(id=self.registro.id).exists())
