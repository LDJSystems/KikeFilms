from django import template
from core.decorators import es_gestor

register = template.Library()

@register.filter
def is_gestor(user):
    return es_gestor(user)