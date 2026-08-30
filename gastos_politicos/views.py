import requests
from django.db.models import Sum
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Governador, Gasto
from .serializers import GovernadorSerializer, GastoSerializer


def consultar_ibge(sigla):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{sigla}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.Timeout:
        return None, "A API do IBGE demorou demais para responder."
    except requests.exceptions.ConnectionError:
        return None, "A API do IBGE está fora do ar."
    except requests.exceptions.HTTPError:
        return None, f"A API do IBGE retornou erro {response.status_code}."
    except requests.exceptions.RequestException as e:
        return None, f"Erro inesperado ao consultar o IBGE: {e}"


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
            dados, erro = consultar_ibge(sigla)
            resultados.append(dados if dados else {"estado": sigla, "erro": erro})

        return Response(resultados, status=status.HTTP_200_OK)


def painel(request):
    """Página de visualização: ranking de gastos por governador + dados do IBGE."""
    governadores_qs = Governador.objects.annotate(
        total_gasto=Sum("gastos__valor")
    ).order_by("-total_gasto")

    maior_total = governadores_qs.first().total_gasto if governadores_qs.exists() else None

    ranking = []
    for g in governadores_qs:
        total = g.total_gasto or 0
        pct = int((total / maior_total) * 100) if maior_total else 0
        ranking.append({"governador": g, "total": total, "pct": pct})

    estados_info = []
    for sigla in Governador.objects.values_list("estado", flat=True).distinct():
        dados, erro = consultar_ibge(sigla)
        estados_info.append(dados if dados else {"sigla": sigla, "erro": erro})

    gastos = Gasto.objects.select_related("governador").order_by("-data")

    return render(request, "gastos_politicos/painel.html", {
        "ranking": ranking,
        "estados_info": estados_info,
        "gastos": gastos,
    })
