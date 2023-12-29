from django.db import models

from apps.testing.abstractions import AbstractFieldDescription
from apps.testing.models.completed_testing import CompletedTesting


class CompletedTask(AbstractFieldDescription):
    serial_number = models.IntegerField(verbose_name='Порядковый номер')
    correct_answer = models.TextField(verbose_name='Правильный ответ')
    user_answer = models.TextField(verbose_name='Ответ пользователя')
    completed_testing = models.ForeignKey(
        CompletedTesting,
        on_delete=models.CASCADE,
        verbose_name='Завершённое тестирование'
    )
