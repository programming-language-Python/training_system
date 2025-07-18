from django.db import models

from abstractions.abstract_fields import AbstractFieldWeight
from abstractions.abstract_models import AbstractTask


class Task(AbstractFieldWeight, AbstractTask):
    RELATED_NAME = 'task_set'

    testing = models.ForeignKey(
        'Testing',
        related_name=RELATED_NAME,
        on_delete=models.CASCADE,
        verbose_name='Тестирование'
    )
    setting = models.ForeignKey(
        'Setting',
        related_name=RELATED_NAME,
        on_delete=models.CASCADE,
        verbose_name='Настройка'
    )

    class Meta(AbstractTask.Meta):
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
