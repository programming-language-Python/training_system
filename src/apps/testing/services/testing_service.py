from abstractions.abstract_services import AbstractTestingService
from apps.base_testing.services import MaxScoreService
from apps.testing.models import SolvingTesting, SolvingTask, Task


class TestingService(AbstractTestingService):
    def _get_or_create_solving_testing(self) -> tuple[SolvingTesting, bool]:
        return SolvingTesting.objects.get_or_create(
            testing_id=self.testing_pk,
            student_id=self.student_pk,
        )

    def _create_solving_task(self, task: Task) -> None:
        solving_task_data = {
            'task': task,
            'solving_testing': self.solving_testing
        }
        solving_task, is_created = SolvingTask.objects.get_or_create(**solving_task_data)
        testing = self.solving_testing.testing
        is_set_time = is_created and not testing.lead_time
        if is_set_time:
            if testing.task_lead_time:
                solving_task.time_left = testing.task_lead_time
            else:
                solving_task.time_left = task.lead_time
            solving_task.save()

    def _calculate_assessment(self) -> int:
        max_score_service = MaxScoreService(
            max_score=self.solving_testing.testing.max_score
        )
        percentage_execution = self.solving_testing.get_percentage_execution()
        return max_score_service.get_assessment(percentage_execution)
