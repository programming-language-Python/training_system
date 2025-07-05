from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar, Generic

from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

SolvingTestingT = TypeVar('SolvingTestingT')


class AbstractTestingService(ABC):
    testing_pk: int
    student_pk: int
    solving_testing: SolvingTestingT

    def __init__(self, testing_pk: int, student_pk: int):
        self.testing_pk = testing_pk
        self.student_pk = student_pk

    @property
    def solving_tasks(self) -> QuerySet:
        return self.solving_testing.solving_task_set.all()

    def get_solving_testing(self) -> SolvingTestingT:
        return self.solving_testing

    def is_time_up(self) -> bool:
        if self.solving_testing.end_passage is None:
            return False
        return self.solving_testing.end_passage <= datetime.now()

    def start_testing(self) -> None:
        self.solving_testing, is_created = self._get_or_create_solving_testing()
        if is_created:
            self._create_solving_tasks()
            quantity_tasks = self.solving_testing.solving_task_set.count()
            self.solving_testing.set_end_passage(quantity_tasks)

    def _create_solving_tasks(self) -> None:
        for task in self.solving_testing.testing.task_set.all():
            self._create_solving_task(task)

    @abstractmethod
    def _create_solving_task(self, task) -> None:
        pass

    def end_testing(self) -> HttpResponseRedirect:
        self.solving_testing.assessment = self._calculate_assessment()
        self.solving_testing.end_passage = datetime.now()
        self.solving_testing.save()
        return redirect('user:home')

    @abstractmethod
    def _calculate_assessment(self) -> int:
        pass

    @abstractmethod
    def _get_or_create_solving_testing(self) -> tuple[SolvingTestingT, bool]:
        pass
