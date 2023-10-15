from django.db import models

from abstractions.abstract_fields import AbstractFieldWeight
from apps.testing.abstractions import AbstractFieldText


class Sequencing(AbstractFieldText, AbstractFieldWeight):
    pass


class CorrectAnswer(AbstractFieldText):
    order = models.IntegerField(verbose_name='Порядок')
    sequencing = models.ForeignKey(
        Sequencing,
        on_delete=models.CASCADE,
        verbose_name='Правильный ответ'
    )


class IncorrectAnswer(AbstractFieldText):
    sequencing = models.ForeignKey(
        Sequencing,
        on_delete=models.CASCADE,
        verbose_name='Не правильный ответ'
    )
