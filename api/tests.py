from rest_framework.test import APITestCase
from rest_framework import status
from .models import TipoSigno


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