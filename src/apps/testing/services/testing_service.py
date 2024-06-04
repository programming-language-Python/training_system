import datetime
from typing import Type

from django.db.models import QuerySet
from django.forms import ModelForm
from django.shortcuts import redirect

from apps.testing.forms.task_forms.open_question_form import SolvingOpenQuestionForm
from apps.testing.forms.task_forms.сlosed_question_form import SolvingClosedQuestionForm
from apps.testing.models import SolvingTesting
from apps.testing.models.solving_tasks import SolvingOpenQuestion, SolvingClosedQuestion
from apps.testing.models.tasks import OpenQuestion, ClosedQuestion
from apps.testing.services import TaskService
from apps.testing.types import SolvingTestingData, TaskFormData, PageData
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
        self.solving_testing, is_created = SolvingTesting.objects.get_or_create(
            testing_id=self.testing_pk,
            student=student
        )
        task_forms = []
        pages = []
        for task in self.sort_tasks_serial_number():
            form, page = self.get_solving_task_form(task)
            task_forms.append(form)
            pages.append(page)
        task_form_data = TaskFormData(self, pages)
        solving_testing_data = SolvingTestingData(task_forms, task_form_data)
        return solving_testing_data

    def get_solving_task_form(self, task: QuerySet) -> tuple[Type[ModelForm], PageData]:
        solving_task_data = {
            'task': task,
            'solving_testing': self.solving_testing
        }
        if isinstance(task, OpenQuestion):
            solving_task, is_created = SolvingOpenQuestion.objects.get_or_create(
                **solving_task_data
            )
            form = SolvingOpenQuestionForm
        elif isinstance(task, ClosedQuestion):
            solving_task, is_created = SolvingClosedQuestion.objects.get_or_create(
                **solving_task_data
            )
            form = SolvingClosedQuestionForm
        else:
            raise NotImplementedError('Такого типа задачи не существует')
        page_data = PageData(
            answer=solving_task.answer,
            solving_task=solving_task
        )
        return form, page_data

    def end_testing(self, task_forms) -> redirect:
        self.solving_testing.end_passage = datetime.datetime.now()
        self.solving_testing.assessment = self.get_assessment(task_forms)
        self.solving_testing.save()
        return redirect('user:home')

    def get_assessment(self, task_forms) -> float:
        for task_form in task_forms:
            task = task_form.initial['solving_task'].task
            answer = task_form.cleaned_data['answer']
            self.set_weight(task, answer)
        assessment = round_up(self.weight / len(task_forms) * 5)
        return assessment

    def set_weight(self, task, answer) -> None:
        if task.task_type.name == 'Открытый вопрос':
            is_correct_answer = task.open_question_answer_option_set.filter(
                correct_answer=answer
            ).exists()
            self.weight += 1 if is_correct_answer else 0

    @staticmethod
    def update_solving_task(solving_task, cleaned_data) -> None:
        if solving_task.task.task_type.name == 'Открытый вопрос':
            solving_task.answer = cleaned_data['answer']
            solving_task.save()
