from django.http import HttpRequest

from abstractions.abstract_views import AbstractStudentSolvingTestingDetailView
from apps.testing.models import SolvingTask
from apps.testing.services import TaskService, TestingService
from apps.testing.types import TaskType


class StudentSolvingTestingDetailView(AbstractStudentSolvingTestingDetailView):
    model = SolvingTask
    template_name = 'testing/student_solving_testing_detail.html'

    def _initialize_service(self, testing_pk: int, student_pk: int) -> None:
        self.testing_service = TestingService(testing_pk, student_pk)

    def _get_solving_task_form(self, solving_task: SolvingTask.objects):
        return solving_task.task.service.get_solving_form(
            solving_testing_pk=self.testing_service.solving_testing.pk,
        )

    @staticmethod
    def _save_answer(request: HttpRequest, solving_task) -> None:
        if solving_task.task.task_type == TaskType.OPEN_QUESTION:
            answer = request.POST.get('answer')
        else:
            answer = request.POST.getlist('answer')
        task_service = TaskService()
        task_service.save_answer(solving_task, answer)
