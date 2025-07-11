from django.db import models
from django.db.models import Sum
from django.urls import reverse

from abstractions.abstract_models.abstract_testing import AbstractTesting


class Testing(AbstractTesting):
    total_weight = models.IntegerField(default=0, verbose_name='Общий вес')

    def get_absolute_url(self) -> reverse:
        return reverse('testing_by_code:testing_detail', kwargs={'pk': self.pk})

    def get_student_absolute_url(self) -> reverse:
        return reverse(f'testing_by_code:student_testing_detail', kwargs={'pk': self.pk})

    def get_total_weight(self) -> int:
        return self.task_set.aggregate(
            total_weight=Sum('weight')
        )['total_weight']

    def is_solving_testing_set(self) -> bool:
        return self.testing_by_code_solving_testing_set.exists()

    def __str__(self):
        return self.title

    class Meta(AbstractTesting.Meta):
        pass
