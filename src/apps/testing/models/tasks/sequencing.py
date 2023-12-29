from django.db import models

from abstractions.abstract_fields import AbstractFieldWeight
from apps.testing.abstractions import AbstractFieldDescription
from apps.testing.models import Testing


class Sequencing(AbstractFieldDescription, AbstractFieldWeight):
    testing = models.ForeignKey(
        Testing,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Тестирование'
    )


class CorrectAnswer(AbstractFieldDescription):
    order = models.IntegerField(verbose_name='Порядок')
    sequencing = models.ForeignKey(
        Sequencing,
        on_delete=models.CASCADE,
        verbose_name='Правильный ответ'
    )


class IncorrectAnswer(AbstractFieldDescription):
    sequencing = models.ForeignKey(
        Sequencing,
        on_delete=models.CASCADE,
        verbose_name='Не правильный ответ'
    )
