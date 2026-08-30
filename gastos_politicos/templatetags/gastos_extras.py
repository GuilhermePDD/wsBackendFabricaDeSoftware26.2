from django import template

register = template.Library()


@register.filter
def brl(valor):
    """Formata um número no padrão monetário brasileiro: 1.234.567,89"""
    texto = f"{float(valor):,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return texto


@register.filter
def brl_compacto(valor):
    """Formata um número de forma resumida: 77.11B, 4.20M, 850.00K"""
    valor = float(valor)
    if valor >= 1_000_000_000:
        return f"{valor / 1_000_000_000:.2f}B"
    if valor >= 1_000_000:
        return f"{valor / 1_000_000:.2f}M"
    if valor >= 1_000:
        return f"{valor / 1_000:.2f}K"
    return f"{valor:.2f}"
