from django.db import models


class Governador(models.Model):
    nome = models.CharField(max_length=150)
    partido = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)
    inicio_mandato = models.DateField()
    fim_mandato = models.DateField()

    def __str__(self):
        return f"{self.nome} ({self.estado})"


class Gasto(models.Model):
    governador = models.ForeignKey(
        Governador,
        on_delete=models.PROTECT,
        related_name="gastos",
    )
    categoria = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField()
    orgao = models.CharField(max_length=150)
    fonte_url = models.URLField()

    def __str__(self):
        return f"{self.categoria} - {self.valor} ({self.governador})"
