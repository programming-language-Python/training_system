from django.db import models

from apps.testing.abstractions.abstract_models.abstract_answer_options import AbstractAnswerOption


class AbstractAnswerOptionWithCheckbox(AbstractAnswerOption):
    is_correct = models.BooleanField(verbose_name='Правильный')

    class Meta(AbstractAnswerOption.Meta):
        abstract = True
