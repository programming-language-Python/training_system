from django.db import models

from abstractions.abstract_models import AbstractSolvingTask
from apps.testing.constants import APP_NAME
from apps.testing.models.solving_testing import SolvingTesting


class SolvingOpenQuestion(AbstractSolvingTask):
    RELATED_NAME = 'solving_open_question_set'

    task = models.ForeignKey(
        'OpenQuestion',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Открытый вопрос'
    )
    solving_testing = models.ForeignKey(
        SolvingTesting,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Решение тестирования'
    )

    class Meta:
        db_table = f'{APP_NAME}_solving-open-question'
