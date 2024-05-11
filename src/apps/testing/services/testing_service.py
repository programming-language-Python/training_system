import datetime

from django.db.models import QuerySet
from django.shortcuts import redirect

from apps.testing.forms.task_forms.open_question_form import OpenQuestionAnswerForm
from apps.testing.models import SolvingTesting
from apps.testing.models.solving_tasks import SolvingOpenQuestion
from apps.testing.models.tasks import OpenQuestion
from apps.testing.services import TaskService
from apps.testing_by_code.utils.utils import round_up
from apps.user.models import Student


class TestingService(TaskService):
    weight: int
    solving_testing: SolvingTesting

    def __init__(self, testing_pk: int):
        super().__init__(testing_pk)
        self.weight = 0

    def start_testing(self, student: Student):
        self.solving_testing, is_created = SolvingTesting.objects.get_or_create(
            testing_id=self.testing_pk,
            student=student
        )
        task_forms = []
        form_task_data = {
            'solving_testing': self.solving_testing
        }
        for page, task in enumerate(self.sort_tasks_serial_number()):
            form, form_data = self.create_solving_task(task, page)
            task_forms.append(form)
            form_task_data |= form_data
        return task_forms, form_task_data

    def create_solving_task(self, task: QuerySet, page: int):
        if isinstance(task, OpenQuestion):
            solving_task, is_created = SolvingOpenQuestion.objects.get_or_create(
                task=task,
                solving_testing=self.solving_testing
            )
            form = OpenQuestionAnswerForm
        else:
            raise NotImplementedError('Такого типа задачи не существует')
        form_data = {
            page: {
                'solving_task': solving_task,
                'answer': solving_task.answer
            }
        }
        return form, form_data

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
