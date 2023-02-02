from django import template

register = template.Library()


@register.simple_tag
def get_verbose_name_for_field(instance, field_name):
    """Возвращает verbose_name для поля"""
    return instance._meta.get_field(field_name).verbose_name.title()
