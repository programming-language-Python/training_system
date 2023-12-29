from django.db import models

from abstractions.abstract_models.abstract_completed_testing import AbstractCompletedTesting


class CompletedTesting(AbstractCompletedTesting):
    testing = models.ForeignKey(
        'Testing',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тестирование'
    )
    # TODO удалить tasks. Переделать в models/testing_by_code работу с полем
    #  tasks, чтоб работало как отдельная таблица,
    #  а в самой таблице с помощью Forignkey
    tasks = models.JSONField(verbose_name='Задачи')
