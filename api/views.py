from rest_framework import viewsets
from .models import Paciente, TipoSigno, Dispositivo, RegistroSigno
from .serializers import (
    PacienteSerializer, 
    TipoSignoSerializer, 
    DispositivoSerializer, 
    RegistroSignoSerializer
)

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class TipoSignoViewSet(viewsets.ModelViewSet):
    queryset = TipoSigno.objects.all()
    serializer_class = TipoSignoSerializer

class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer

class RegistroSignoViewSet(viewsets.ModelViewSet):
    queryset = RegistroSigno.objects.all()
    serializer_class = RegistroSignoSerializer
