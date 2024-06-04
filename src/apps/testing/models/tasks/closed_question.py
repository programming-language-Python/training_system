from django.db import models
from django.db.models import QuerySet

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
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Тип задачи'
    )
    testing = models.ForeignKey(
        Testing,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Тестирование'
    )

    def get_answer_options(self) -> QuerySet:
        return self.closed_question_answer_option_set.all()

    class Meta(AbstractTask.Meta):
        db_table = f'{APP_NAME}_closed-question'
