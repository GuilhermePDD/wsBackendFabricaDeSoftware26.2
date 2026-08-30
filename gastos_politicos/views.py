import requests
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Governador, Gasto
from .serializers import GovernadorSerializer, GastoSerializer


class GovernadorViewSet(viewsets.ModelViewSet):
    queryset = Governador.objects.all()
    serializer_class = GovernadorSerializer


class GastoViewSet(viewsets.ModelViewSet):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer


class EstadosInfoView(APIView):
    """Consulta a API do IBGE para cada estado já cadastrado em Governador."""

    def get(self, request):
        siglas = Governador.objects.values_list("estado", flat=True).distinct()
        resultados = []

        for sigla in siglas:
            url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{sigla}"
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                resultados.append(response.json())
            except requests.exceptions.Timeout:
                resultados.append({"estado": sigla, "erro": "A API do IBGE demorou demais para responder."})
            except requests.exceptions.ConnectionError:
                resultados.append({"estado": sigla, "erro": "A API do IBGE está fora do ar."})
            except requests.exceptions.HTTPError:
                resultados.append({"estado": sigla, "erro": f"A API do IBGE retornou erro {response.status_code}."})
            except requests.exceptions.RequestException as e:
                resultados.append({"estado": sigla, "erro": f"Erro inesperado ao consultar o IBGE: {e}"})

        return Response(resultados, status=status.HTTP_200_OK)
