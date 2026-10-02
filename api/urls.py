from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PacienteViewSet,
    TipoSignoViewSet,
    DispositivoViewSet,
    RegistroSignoViewSet,
)

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'tipos-signo', TipoSignoViewSet, basename='tiposigno')
router.register(r'dispositivos', DispositivoViewSet, basename='dispositivo')
router.register(r'registros', RegistroSignoViewSet, basename='registro')

urlpatterns = [
    path('', include(router.urls)),
]