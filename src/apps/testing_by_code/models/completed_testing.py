from django.db import models

from abstractions.abstract_models.abstract_completed_testing import AbstractCompletedTesting
from apps.testing_by_code.utils.utils import round_up


class CompletedTesting(AbstractCompletedTesting):
    total_weight = models.IntegerField(verbose_name='Общий вес')
    weight_of_student_tasks = models.IntegerField(verbose_name='Вес задач студента')
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

    def get_assessment_in_percentage(self):
        return round_up(self.weight_of_student_tasks / self.total_weight * 100)
