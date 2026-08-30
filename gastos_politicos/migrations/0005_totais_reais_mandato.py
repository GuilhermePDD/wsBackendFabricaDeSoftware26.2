from django.db import migrations
from datetime import date

FONTE = "https://dados.pb.gov.br/en/dataset/despesas/resource/07ac5407-a7f4-4824-9740-b16d3e72098c"
CATEGORIA = "Total apurado do mandato (todos os órgãos, elaboração própria via API oficial)"
ORGAO = "Governo do Estado da Paraíba - todos os órgãos"


def substituir(apps, schema_editor):
    Governador = apps.get_model("gastos_politicos", "Governador")
    Gasto = apps.get_model("gastos_politicos", "Gasto")

    # remove as amostras de 1 registro por mandato (migration 0003)
    Gasto.objects.filter(categoria__in=["Educação", "Saúde"]).delete()

    totais = [
        ("Ricardo Coutinho", date(2015, 1, 1), "47807675002.90", date(2018, 12, 31)),
        ("João Azevêdo", date(2019, 1, 1), "61246373953.76", date(2022, 12, 31)),
        ("João Azevêdo", date(2023, 1, 1), "77115197185.87", date(2026, 3, 31)),
        ("Lucas Ribeiro", date(2026, 4, 2), "11283408684.32", date(2026, 8, 30)),
    ]

    for nome, inicio, valor, data_apuracao in totais:
        governador = Governador.objects.get(nome=nome, inicio_mandato=inicio)
        Gasto.objects.create(
            governador=governador,
            categoria=CATEGORIA,
            valor=valor,
            data=data_apuracao,
            orgao=ORGAO,
            fonte_url=FONTE,
        )


def reverter(apps, schema_editor):
    Gasto = apps.get_model("gastos_politicos", "Gasto")
    Gasto.objects.filter(categoria=CATEGORIA).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("gastos_politicos", "0004_alter_gasto_valor"),
    ]

    operations = [
        migrations.RunPython(substituir, reverter),
    ]
