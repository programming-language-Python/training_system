from django.db import models

from abstractions.abstract_fields import AbstractFieldWeight
from apps.testing.abstractions import AbstractFieldText


class OpenQuestion(AbstractFieldText, AbstractFieldWeight):
    correct_answer = models.TextField(verbose_name='Правильный ответ')

    class Meta(AbstractFieldText.Meta, AbstractFieldWeight.Meta):
        pass
