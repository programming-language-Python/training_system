from django.db import models

from abstractions.abstract_models.abstract_solving_testing import AbstractSolvingTesting
from apps.testing_by_code.constants import APP_NAME
from utils import round_up


class SolvingTesting(AbstractSolvingTesting):
    earned_weight = models.IntegerField(null=True, verbose_name='Заработанный вес')

    def get_assessment_in_percentage(self) -> int:
        return round_up(self.earned_weight / self.testing.get_total_weight() * 100)

    class Meta(AbstractSolvingTesting.Meta):
        db_table = f'{APP_NAME}_solving-testing'
