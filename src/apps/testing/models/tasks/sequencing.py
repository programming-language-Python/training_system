from django.db import models

from abstractions.abstract_models import AbstractTask
from apps.testing.models import Testing
from apps.testing.models.tasks import TaskType


class Sequencing(AbstractTask):
    RELATED_NAME = 'sequencing_set'

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
