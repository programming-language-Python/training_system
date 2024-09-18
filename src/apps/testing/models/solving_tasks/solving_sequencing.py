from django.db import models

from abstractions.abstract_models import AbstractSolvingTask
from apps.testing.constants import APP_NAME
from apps.testing.models import SolvingTesting


class SolvingSequencing(AbstractSolvingTask):
    RELATED_NAME = 'solving_sequencing_set'

    task = models.ForeignKey(
        'Sequencing',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Установление последовательности'
    )
    solving_testing = models.ForeignKey(
        SolvingTesting,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Решение тестирования'
    )

    def set_answer(self, answer: str) -> None:
        self.answer = answer
        self.save()

    class Meta:
        db_table = f'{APP_NAME}_solving-sequencing'
