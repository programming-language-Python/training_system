import random

from django import template

register = template.Library()


@register.simple_tag
def random_code(code_template):
    """Выбирает случайным образом код code кода шаблона code_template"""
    return random.choices(code_template)[0].code
