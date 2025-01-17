from typing import Iterable

from django.db import models

from apps.testing.constants import APP_NAME
from services import get_field_values


class ClosedQuestion(models.Model):
    RELATED_NAME = 'closed_question_set'

    is_several_correct_answers = models.BooleanField(
        default=False,
        verbose_name='Несколько правильных ответов'
    )
    is_random_order_answer_options = models.BooleanField(
        default=False,
        verbose_name='Случайный порядок вариантов ответа'
    )
    is_partially_correct_execution = models.BooleanField(
        default=False,
        verbose_name='Учет частично верного выполнения'
    )
    task = models.OneToOneField(
        'Task',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Задача'
    )

    def get_fields(self) -> Iterable:
        return get_field_values(
            model=self,
            excluded_fields=['id', 'task']
        )

    class Meta:
        db_table = f'{APP_NAME}_closed-question'
