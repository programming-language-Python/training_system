from django.http import HttpRequest

from abstractions.abstract_views import AbstractStudentSolvingTestingDetailView
from apps.testing.models import SolvingTask
from apps.testing.services import TestingService


class StudentSolvingTestingDetailView(AbstractStudentSolvingTestingDetailView):
    model = SolvingTask
    template_name = 'testing/student_solving_testing_detail.html'

    def _initialize_service(self, testing_pk: int, student_pk: int) -> None:
        self.testing_service = TestingService(testing_pk, student_pk)

    def _get_initialized_solving_task_form(self, solving_task: SolvingTask.objects):
        solving_form = solving_task.task.service.initialize_solving_form(
            solving_testing_pk=self.testing_service.solving_testing.pk,
        )
        return solving_form

    def _save_answer(self, request: HttpRequest, solving_task) -> None:
        form = solving_task.task.service.solving_form(request.POST, instance=solving_task)
        if form.is_valid():
            form.save()
