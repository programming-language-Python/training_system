from datetime import datetime

from django.db.models import QuerySet, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from apps.testing.models import SolvingTesting, SolvingTask, Testing
from apps.testing.types import SolvingTaskEntity
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

    def get_solving_testing(self) -> SolvingTesting:
        return self.solving_testing

    def is_time_up(self) -> bool:
        end_passage = self.solving_testing.end_passage
        if end_passage is None:
            return False
        else:
            return end_passage <= datetime.now()

    def start_testing(self) -> HttpResponseRedirect | QuerySet[SolvingTask]:
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
        solving_tasks = self.solving_testing.solving_task_set
        earned_score = solving_tasks.aggregate(Sum('score'))['score__sum']
        assessment = round_up(earned_score / solving_tasks.count() * 5)
        return assessment
