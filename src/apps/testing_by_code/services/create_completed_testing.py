from typing import Iterable, Mapping

from django.core.handlers.wsgi import WSGIRequest

from apps.testing_by_code import models
from apps.testing_by_code.services.run_code.run_java.run_java import RunJava
from apps.testing_by_code.types import Weight
from apps.testing_by_code.utils.utils import round_up
from apps.user.models import UnfinishedTesting


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

    def execute(self) -> None:
        self._add_tasks()
        request_get = self.request.GET
        title = request_get.get('testing_title')
        start_passage = request_get.get('testing_start_passage')
        testing_pk = request_get.get('testing_pk')
        testing = models.Testing.objects.get(pk=testing_pk)
        is_review_of_result_by_student = request_get.get('testing_is_review_of_result_by_student')
        models.CompletedTesting.objects.create(
            title=title,
            assessment=self._get_assessment(),
            total_weight=self._get_total_weight(),
            weight_of_student_tasks=self.weight_of_student_tasks,
            tasks=self.tasks,
            testing=testing,
            start_passage=start_passage,
            is_review_of_result_by_student=is_review_of_result_by_student,
            student=self.request.user
        )
        self._delete_unfinished_testing(title)

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

    def _delete_unfinished_testing(self, title: str):
        unfinished_testing = UnfinishedTesting.objects.get(
            title=title,
            student=self.request.user
        )
        unfinished_testing.delete()