from rest_framework import viewsets

from .models import Governador, Gasto
from .serializers import GovernadorSerializer, GastoSerializer


class GovernadorViewSet(viewsets.ModelViewSet):
    queryset = Governador.objects.all()
    serializer_class = GovernadorSerializer


class GastoViewSet(viewsets.ModelViewSet):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer
