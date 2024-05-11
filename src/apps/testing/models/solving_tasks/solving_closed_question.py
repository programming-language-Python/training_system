from django.db import models

from abstractions.abstract_models import AbstractSolvingTask
from apps.testing.constants import APP_NAME
from apps.testing.models import SolvingTesting
from apps.testing.models.tasks import ClosedQuestion


class SolvingClosedQuestion(AbstractSolvingTask):
    RELATED_NAME = 'solving_closed_question_set'

    task = models.ForeignKey(
        ClosedQuestion,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Закрытый вопрос'
    )
    solving_testing = models.ForeignKey(
        SolvingTesting,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Решение тестирования'
    )

    class Meta:
        db_table = f'{APP_NAME}_solving-closed-question'
