from django.db.models import Sum

from abstractions.abstract_models import AbstractSolvingTesting
from apps.testing.constants import APP_NAME
from utils import round_up


class SolvingTesting(AbstractSolvingTesting):

    def get_percentage_execution(self) -> int:
        solving_tasks = self.solving_task_set
        earned_score = solving_tasks.aggregate(Sum('score'))['score__sum']
        return round_up(earned_score / solving_tasks.count() * 100)

    class Meta(AbstractSolvingTesting.Meta):
        db_table = f'{APP_NAME}_solving-testing'
