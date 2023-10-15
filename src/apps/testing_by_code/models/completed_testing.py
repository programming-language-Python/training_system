from django.db import models

from abstractions import AbstractCompletedTesting
from apps.testing_by_code.utils.utils import round_up


class CompletedTesting(AbstractCompletedTesting):
    testing = models.ForeignKey(
        'Testing',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тестирование'
    )

    def get_assessment_in_percentage(self):
        return round_up(self.weight_of_student_tasks / self.total_weight * 100)
