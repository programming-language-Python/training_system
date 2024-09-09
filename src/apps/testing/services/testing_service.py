from typing import Sequence, Mapping

from django.shortcuts import redirect

from apps.testing.interfaces import ITask
from apps.testing.models import SolvingTesting
from apps.testing.services import TaskService
from apps.testing.types import SolvingTestingData, TaskFormData, PageData, Task, SolvingTask
from apps.user.models import Student


class TestingService(TaskService):
    solving_testing: SolvingTesting

    def get_solving_testing(self) -> SolvingTesting:
        return self.solving_testing

    def start_testing(self) -> SolvingTestingData:
        task: ITask
        if self.solving_testing is None:
            raise Exception('Не установлена переменная solving_testing')
        pages = []
        task_forms = []
        for task in self.sort_tasks_serial_number():
            pages.append(self.get_page_data(task))
            task_forms.append(task.get_solving_task_form())
        self.solving_testing.set_end_passage(quantity_tasks=len(pages))
        task_form_data = TaskFormData(self, pages)
        return SolvingTestingData(task_forms, task_form_data)

    def set_solving_testing(self, student: Student) -> None:
        self.solving_testing, is_created = SolvingTesting.objects.get_or_create(
            testing_id=self.testing_pk,
            student=student
        )

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
        self.solving_testing.save(task_forms=task_forms)
        return redirect('user:home')

    @staticmethod
    def update_solving_task(solving_task: SolvingTask, cleaned_data: Mapping[str, str]) -> None:
        solving_task.answer = ', '.join(cleaned_data['answer'])
        solving_task.save()
