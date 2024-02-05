import random

from django import template

register = template.Library()


@register.filter
def shuffle(arg):
    args = list(arg)[:]
    random.shuffle(args)
    return args
