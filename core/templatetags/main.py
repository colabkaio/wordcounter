from django import template

register = template.Library()

@register.filter
def porcentagem_de(part, whole):
    try:
        return "{:.2f}%".format((float(part) / whole * 100))
    except (ValueError, ZeroDivisionError):
        return ""