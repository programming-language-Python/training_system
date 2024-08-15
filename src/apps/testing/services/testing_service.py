import datetime
from typing import Iterable, Sequence, Mapping

from django.shortcuts import redirect

from apps.testing.interfaces import ITask
from apps.testing.models import SolvingTesting
from apps.testing.services import TaskService
from apps.testing.types import SolvingTestingData, TaskFormData, PageData, Task, Id, SolvingTask
from apps.testing_by_code.utils.utils import round_up
from apps.user.models import Student


class TestingService(TaskService):
    weight: int
    solving_testing: SolvingTesting

    def __init__(self, testing_pk: int) -> None:
        super().__init__(testing_pk)
        self.weight = 0

    def get_solving_testing(self) -> SolvingTesting:
        return self.solving_testing

    def start_testing(self, student: Student) -> SolvingTestingData:
        task: ITask
        self.solving_testing, is_created = SolvingTesting.objects.get_or_create(
            testing_id=self.testing_pk,
            student=student
        )
        pages = []
        task_forms = []
        for task in self.sort_tasks_serial_number():
            pages.append(self.get_page_data(task))
            task_forms.append(task.get_solving_task_form())
        task_form_data = TaskFormData(self, pages)
        solving_testing_data = SolvingTestingData(task_forms, task_form_data)
        return solving_testing_data

    def get_page_data(self, task: Task) -> PageData:
        solving_task_data = {
            'task': task,
            'solving_testing': self.solving_testing
        }
        solving_task = task.get_or_create_solving_task(solving_task_data)
        page_data = PageData(
            answer=solving_task.answer,
            solving_task=solving_task
        )
        return page_data

    def end_testing(self, task_forms: Sequence[SolvingTask]) -> redirect:
        self.solving_testing.end_passage = datetime.datetime.now()
        self.solving_testing.assessment = self.get_assessment(task_forms)
        self.solving_testing.save()
        return redirect('user:home')

    def get_assessment(self, task_forms: Sequence[SolvingTask]) -> float:
        answer: str | Iterable[Id]
        for task_form in task_forms:
            task = task_form.initial['solving_task'].task
            answer = task_form.cleaned_data['answer']
            self.weight += task.get_weight(answer)
        assessment = round_up(self.weight / len(task_forms) * 5)
        return assessment

    @staticmethod
    def update_solving_task(solving_task: SolvingTask, cleaned_data: Mapping[str, str]) -> None:
        solving_task.answer = cleaned_data['answer']
        solving_task.save()
