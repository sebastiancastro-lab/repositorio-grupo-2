from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PacienteViewSet, 
    TipoSignoViewSet, 
    DispositivoViewSet, 
    RegistroSignoViewSet
)

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'tipos-signo', TipoSignoViewSet)
router.register(r'dispositivos', DispositivoViewSet)
router.register(r'registros-signo', RegistroSignoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]