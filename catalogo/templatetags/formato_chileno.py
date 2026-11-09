from django import template


register = template.Library()


@register.filter
def pesos_chilenos(valor):
    try:
        return f"${int(valor):,}".replace(",", ".")
    except (TypeError, ValueError):
        return valor
