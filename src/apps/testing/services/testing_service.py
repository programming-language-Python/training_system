from datetime import datetime
from typing import Iterable

from django.db.models import QuerySet
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect

from apps.testing.models import SolvingTesting, SolvingTask, Testing
from apps.testing.types import SolvingTaskEntity, Id
from apps.user.models import Student
from utils import round_up


class TestingService:
    testing_pk: int
    student_pk: int
    solving_testing: SolvingTesting
    is_created: bool

    def __init__(self, testing_pk: int, student: Student):
        self.testing_pk = testing_pk
        self.student_pk = student.pk
        self.solving_testing, self.is_created = SolvingTesting.objects.get_or_create(
            testing_id=testing_pk,
            student=student
        )

    def start_testing(self) -> HttpResponseRedirect | QuerySet[SolvingTask]:
        if self.solving_testing.is_time_up():
            raise Http404
        if self.is_created:
            self._create_solving_tasks()
            quantity_tasks = SolvingTask.objects.filter(
                solving_testing__testing=self.testing_pk,
                solving_testing__student=self.student_pk
            ).count()
            self.solving_testing.set_end_passage(quantity_tasks)
        return SolvingTask.objects.filter(
            solving_testing__testing=self.testing_pk,
            solving_testing__student=self.student_pk
        )

    def _create_solving_tasks(self) -> None:
        for task in self._testing.task_set.all():
            self._create_solving_task(task)

    @property
    def _testing(self):
        return Testing.objects.get(pk=self.testing_pk)

    def _create_solving_task(self, task) -> SolvingTaskEntity:
        solving_task_data = {
            'task': task,
            'solving_testing': self.solving_testing
        }
        return SolvingTask.objects.get_or_create(**solving_task_data)

    def end_testing(self) -> redirect:
        self.solving_testing.end_passage = datetime.now()
        self.solving_testing.assessment = self._get_assessment()
        self.solving_testing.save()
        return redirect('user:home')

    def _get_assessment(self) -> float:
        earned_weight = self._get_earned_weight()
        assessment = round_up(earned_weight / self.solving_testing.solving_task_set.count() * 5)
        return assessment

    def _get_earned_weight(self) -> int:
        answer: str | Iterable[Id]
        earned_weight = 0
        for solving_task in self.solving_testing.solving_task_set.all():
            earned_weight += solving_task.task.service.get_weight(
                answer=solving_task.answer
            )
        return earned_weight
