from django.db import models

from abstractions.abstract_fields import AbstractFieldWeight
from abstractions.abstract_models import AbstractTask


class Task(AbstractFieldWeight, AbstractTask):
    RELATED_NAME = 'task_set'

    count = models.IntegerField(
        default=1,
        verbose_name='Количество'
    )
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

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
