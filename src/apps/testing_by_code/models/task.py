from django.db import models
from django.urls import reverse

from abstractions.abstract_fields import AbstractFieldWeight
from apps.testing_by_code.constants import APP_NAME


class Task(AbstractFieldWeight):
    testing = models.ForeignKey(
        'Testing',
        on_delete=models.CASCADE,
        verbose_name='Тестирование'
    )
    setting = models.ForeignKey(
        'Setting',
        on_delete=models.CASCADE,
        verbose_name='Настройка'
    )
    count = models.IntegerField(
        default=0,
        verbose_name='Количество'
    )

    def get_absolut_url(self):
        return reverse(APP_NAME + ':task_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
