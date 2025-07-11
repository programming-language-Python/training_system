from django.http import HttpRequest

from abstractions.abstract_views import AbstractStudentSolvingTestingDetailView
from apps.testing_by_code.forms import SolvingTaskForm
from apps.testing_by_code.models import SolvingTask
from apps.testing_by_code.services import TestingService


class StudentSolvingTestingDetailView(AbstractStudentSolvingTestingDetailView):
    model = SolvingTask
    template_name = 'testing_by_code/student_solving_testing_detail.html'

    def _initialize_service(self, testing_pk: int, student_pk: int) -> None:
        self.testing_service = TestingService(testing_pk, student_pk)

    @staticmethod
    def _save_answer(request: HttpRequest, solving_task) -> None:
        solving_task_form = SolvingTaskForm(request.POST, instance=solving_task)
        if solving_task_form.is_valid():
            solving_task_form.save()

    def _get_solving_task_form(self, solving_task: SolvingTask):
        return SolvingTaskForm(instance=solving_task)
