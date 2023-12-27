from django.db import models

from abstractions.abstract_fields import AbstractFieldWeight
from apps.testing.abstractions.abstract_field_description import AbstractFieldDescription
from apps.testing.models import Testing


class OpenQuestion(AbstractFieldDescription, AbstractFieldWeight):
    correct_answer = models.TextField(verbose_name='Правильный ответ')
    testing = models.ForeignKey(
        Testing,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Тестирование'
    )

    class Meta(AbstractFieldDescription.Meta, AbstractFieldWeight.Meta):
        pass
