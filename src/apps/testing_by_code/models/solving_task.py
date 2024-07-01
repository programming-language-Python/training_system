from django.db import models

from abstractions.abstract_models import AbstractSolvingTask
from apps.testing_by_code.constants import APP_NAME
from apps.testing_by_code.models import SolvingTesting, Task


class SolvingTask(AbstractSolvingTask):
    RELATED_NAME = 'solving_task_set'

    code = models.TextField(verbose_name='Код')
    correct_answer = models.CharField(
        max_length=100,
        verbose_name='Правильный ответ'
    )
    solving_testing = models.ForeignKey(
        SolvingTesting,
        related_name=RELATED_NAME,
        on_delete=models.CASCADE,
        verbose_name='Тестирование'
    )
    task = models.ForeignKey(
        Task,
        related_name=RELATED_NAME,
        on_delete=models.CASCADE,
        verbose_name='Задача'
    )

    def is_correctly_resolved(self) -> bool:
        return self.correct_answer == self.answer

    class Meta:
        db_table = f'{APP_NAME}_solving-task'
