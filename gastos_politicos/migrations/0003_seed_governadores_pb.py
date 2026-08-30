from django.db import migrations
from datetime import date


def criar_dados(apps, schema_editor):
    Governador = apps.get_model("gastos_politicos", "Governador")
    Gasto = apps.get_model("gastos_politicos", "Gasto")

    coutinho_2 = Governador.objects.create(
        nome="Ricardo Coutinho",
        partido="PSB",
        estado="PB",
        inicio_mandato=date(2015, 1, 1),
        fim_mandato=date(2019, 1, 1),
    )
    azevedo_1 = Governador.objects.create(
        nome="João Azevêdo",
        partido="PSB",
        estado="PB",
        inicio_mandato=date(2019, 1, 1),
        fim_mandato=date(2023, 1, 1),
    )
    azevedo_2 = Governador.objects.create(
        nome="João Azevêdo",
        partido="PSB",
        estado="PB",
        inicio_mandato=date(2023, 1, 1),
        fim_mandato=date(2026, 4, 2),
    )
    Governador.objects.create(
        nome="Lucas Ribeiro",
        partido="Progressistas",
        estado="PB",
        inicio_mandato=date(2026, 4, 2),
        fim_mandato=None,
    )

    Gasto.objects.create(
        governador=coutinho_2,
        categoria="Educação",
        valor="50752513.38",
        data=date(2015, 1, 30),
        orgao="Secretaria de Estado da Educação",
        fonte_url="https://api.dados.pb.gov.br/api/v1/despesas/orcamentarias?ano=2015&mes=01",
    )
    Gasto.objects.create(
        governador=azevedo_2,
        categoria="Saúde",
        valor="115207413.60",
        data=date(2025, 6, 25),
        orgao="Secretaria de Estado da Saúde",
        fonte_url="https://api.dados.pb.gov.br/api/v1/despesas/orcamentarias?ano=2025&mes=06",
    )


def remover_dados(apps, schema_editor):
    Governador = apps.get_model("gastos_politicos", "Governador")
    Governador.objects.filter(estado="PB", nome__in=[
        "Ricardo Coutinho", "João Azevêdo", "Lucas Ribeiro",
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("gastos_politicos", "0002_alter_governador_fim_mandato"),
    ]

    operations = [
        migrations.RunPython(criar_dados, remover_dados),
    ]
