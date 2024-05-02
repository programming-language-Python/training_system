from django.db import models

from abstractions.abstract_models import AbstractTask
from apps.testing.constants import APP_NAME
from apps.testing.models import Testing
from apps.testing.models.tasks import TaskType


class ClosedQuestion(AbstractTask):
    RELATED_NAME = 'closed_question_set'

    is_several_correct_answers = models.BooleanField(
        default=False,
        verbose_name='Допустимо несколько правильных ответов'
    )
    is_random_order_answer_options = models.BooleanField(
        default=False,
        verbose_name='Случайный порядок вариантов ответа'
    )
    is_partially_correct_execution = models.BooleanField(
        default=False,
        verbose_name='При оценке учесть частично правильное выполнение задания'
    )
    task_type = models.OneToOneField(
        TaskType,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Тип задачи'
    )
    testing = models.ManyToManyField(
        Testing,
        related_name=RELATED_NAME,
        verbose_name='Тестирование'
    )

    class Meta:
        db_table = f'{APP_NAME}_closed-question'
