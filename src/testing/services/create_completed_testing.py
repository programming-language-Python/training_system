from typing import Iterable, Mapping

from django.core.handlers.wsgi import WSGIRequest

from testing import models
from testing.services.generate_code.types import Weight
from testing.services.run_code.run_java.run_java import RunJava
from testing.utils.utils import round_up


class CreateCompletedTesting:
    request: WSGIRequest
    task_weights: Iterable[Weight]
    task_weight: Weight
    weight_of_student_tasks: Weight
    user_answers: Iterable[str]
    user_answer: str
    codes: Iterable[str]
    code: str
    tasks: list[Mapping[str, str]]

    def __init__(self, request: WSGIRequest) -> None:
        self.request = request
        self.task_weights = [int(task_weight) for task_weight in request.GET.getlist('weight')]
        self.user_answers = request.GET.getlist('answer')
        self.codes = request.GET.getlist('code')
        self.weight_of_student_tasks = 0
        self.tasks = []

    def execute(self):
        self._add_tasks()
        models.CompletedTesting.objects.create(
            assessment=self._get_assessment(),
            total_weight=self._get_total_weight(),
            weight_of_student_tasks=self.weight_of_student_tasks,
            tasks=self.tasks,
            testing=self._get_testing(),
            student=self.request.user
        )
        # TODO Расскоментить?
        # self._delete_session()

    def _add_tasks(self):
        for self.task_weight, self.user_answer, self.code in zip(self.task_weights, self.user_answers, self.codes):
            self._add_task()

    def _add_task(self):
        run_java = RunJava(self.code)
        raw_answer = run_java.execute()
        answer = "".join(raw_answer.split())
        if answer == self.user_answer:
            self.weight_of_student_tasks += self.task_weight
        task = {
            'weight': self.task_weight,
            'code': self.code,
            'answer': answer,
            'user_answer': self.user_answer
        }
        self.tasks.append(task)

    def _get_assessment(self):
        return round_up(self.weight_of_student_tasks / sum(self.task_weights) * 5)

    def _get_total_weight(self):
        return sum(self.task_weights)

    def _get_testing(self):
        return models.Testing.objects.get(pk=self.request.GET.get('testing_pk'))

    def _delete_session(self):
        session_name = 'testing_' + str(self.request.GET.get('testing_pk'))
        del self.request.session[session_name]
