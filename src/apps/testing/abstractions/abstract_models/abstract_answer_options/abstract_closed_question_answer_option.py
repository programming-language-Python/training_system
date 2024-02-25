from django.db import models

from apps.testing.abstractions.abstract_models.abstract_answer_options import AbstractAnswerOption


class AbstractClosedQuestionAnswerOption(AbstractAnswerOption):
    is_correct = models.BooleanField(verbose_name='Правильный')

    class Meta:
        abstract = True
