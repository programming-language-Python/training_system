from datetime import datetime
from typing import Sequence, Iterable

from django.shortcuts import redirect

from apps.testing.models import SolvingTesting, SolvingTask, Testing, Task
from apps.testing.services import TaskFormService, TaskService
from apps.testing.types import SolvingTestingData, SolvingTaskEntity, Id
from apps.testing_by_code.utils.utils import round_up
from apps.user.models import Student


class TestingService:
    testing_pk: int
    student_pk: int
    solving_testing: SolvingTesting

    def __init__(self, testing_pk: int, student: Student):
        self.testing_pk = testing_pk
        self.student_pk = student.pk
        self.solving_testing, is_created = SolvingTesting.objects.get_or_create(
            testing_id=testing_pk,
            student=student
        )

    def start_testing(self) -> SolvingTestingData:
        if self.solving_testing.is_time_up():
            return redirect('user:student_solving_testing_list', pk=self.student_pk)
        page_data = {}
        task_forms = []
        for i, task in enumerate(self._testing.task_set.all()):
            page_data[i] = self._get_solving_task(task)
            task_forms.append(self._get_solving_task_form(task_type=task.type))
        self.solving_testing.set_end_passage(quantity_tasks=len(page_data))
        return SolvingTestingData(task_forms, page_data)

    @property
    def _testing(self):
        return Testing.objects.get(pk=self.testing_pk)

    def _get_solving_task(self, task: Task) -> SolvingTaskEntity:
        solving_task_data = {
            'task': task,
            'solving_testing': self.solving_testing
        }
        solving_task, is_created = SolvingTask.objects.get_or_create(**solving_task_data)
        return solving_task

    @staticmethod
    def _get_solving_task_form(task_type: str):
        task_form_service = TaskFormService()
        return task_form_service.get_solving_form(task_type)

    def end_testing(self, task_forms: Sequence[SolvingTask]) -> redirect:
        if task_forms:
            self.solving_testing.end_passage = datetime.now()
            self.solving_testing.assessment = self._get_assessment(task_forms)
        self.solving_testing.save()
        return redirect('user:home')

    def _get_assessment(self, task_forms: Sequence[SolvingTask]) -> float:
        earned_weight = self._get_earned_weight(task_forms)
        assessment = round_up(earned_weight / len(task_forms) * 5)
        return assessment

    @staticmethod
    def _get_earned_weight(task_forms):
        answer: str | Iterable[Id]
        earned_weight = 0
        task_service = TaskService()
        for i, task_form in enumerate(task_forms):
            task = task_form.initial[i].task
            answer = task_form.cleaned_data['answer']
            earned_weight += task_service.get_weight(task, answer)
        return earned_weight
