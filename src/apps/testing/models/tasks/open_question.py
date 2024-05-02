from django.db import models

from abstractions.abstract_models import AbstractTask
from apps.testing.constants import APP_NAME
from apps.testing.models import Testing
from apps.testing.models.tasks import TaskType


class OpenQuestion(AbstractTask):
    RELATED_NAME = 'open_question_set'

    task_type = models.OneToOneField(
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

    class Meta:
        db_table = f'{APP_NAME}_open-question'
