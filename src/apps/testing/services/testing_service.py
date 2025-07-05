from django.db.models import Sum

from abstractions.abstract_services import AbstractTestingService
from apps.testing.models import SolvingTesting, SolvingTask
from apps.testing.types import SolvingTaskEntity
from utils import round_up


class TestingService(AbstractTestingService):
    def _get_or_create_solving_testing(self) -> tuple[SolvingTesting, bool]:
        return SolvingTesting.objects.get_or_create(
            testing_id=self.testing_pk,
            student_id=self.student_pk,
        )

    def _create_solving_task(self, task) -> SolvingTaskEntity:
        solving_task_data = {
            'task': task,
            'solving_testing': self.solving_testing
        }
        return SolvingTask.objects.get_or_create(**solving_task_data)

    def _calculate_assessment(self) -> int:
        solving_tasks = self.solving_testing.solving_task_set
        earned_score = solving_tasks.aggregate(Sum('score'))['score__sum']
        assessment = round_up(earned_score / solving_tasks.count() * 5)
        return assessment
