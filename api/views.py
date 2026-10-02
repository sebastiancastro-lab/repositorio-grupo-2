from django.db.models import ProtectedError
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Paciente, TipoSigno, Dispositivo, RegistroSigno
from .serializers import (
    PacienteSerializer,
    TipoSignoSerializer,
    DispositivoSerializer,
    RegistroSignoSerializer,
)

class ProtegidoMixin:
    """Si el objeto ya tiene registros de signos asociados, responde 409 en lugar de un error 500."""

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'detail': 'No se puede eliminar: tiene registros de signos asociados.'},
                status=status.HTTP_409_CONFLICT,
            )


class PacienteViewSet(ProtegidoMixin, viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


class TipoSignoViewSet(ProtegidoMixin, viewsets.ModelViewSet):
    queryset = TipoSigno.objects.all()
    serializer_class = TipoSignoSerializer


class DispositivoViewSet(ProtegidoMixin, viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        estado = self.request.query_params.get('estado')
        if estado:
            qs = qs.filter(estado=estado)
        return qs


class RegistroSignoViewSet(viewsets.ModelViewSet):
    serializer_class = RegistroSignoSerializer

    def get_queryset(self):
        qs = RegistroSigno.objects.select_related('paciente', 'tipo_signo', 'dispositivo')
        for campo in ('paciente', 'tipo_signo', 'dispositivo'):
            valor = self.request.query_params.get(campo)
            if valor and valor.isdigit():
                qs = qs.filter(**{f'{campo}_id': int(valor)})
        return qs
