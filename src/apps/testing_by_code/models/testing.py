from django.db.models import Sum, F
from django.urls import reverse

from abstractions.abstract_models.abstract_testing import AbstractTesting
from apps.testing_by_code.constants import APP_NAME


class Testing(AbstractTesting):

    def get_absolute_url(self) -> reverse:
        return reverse(APP_NAME + ':testing_detail', kwargs={'pk': self.pk})

    def get_total_weight(self) -> int:
        return self.task_set.annotate(
            total_task_weight=F('weight') * F('count')
        ).aggregate(
            total_weight=Sum('total_task_weight')
        )['total_weight']

    def __str__(self):
        return self.title

    class Meta(AbstractTesting.Meta):
        pass
