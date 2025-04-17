from datetime import datetime
from typing import Iterable

from django.db import models

from abstractions.abstract_models.abstract_solving_testing import AbstractSolvingTesting
from apps.testing_by_code.constants import APP_NAME
from utils import round_up


class SolvingTesting(AbstractSolvingTesting):
    earned_weight = models.IntegerField(null=True, verbose_name='Заработанный вес')

    def complete(self, answers: Iterable[str]) -> None:
        self._set_answers(answers)
        self._set_earned_weight()
        self._set_assessment()
        self._set_end_passage()
        self.save()

    def _set_answers(self, answers: Iterable[str]) -> None:
        for solving_task, answer in zip(self.solving_task_set.all(), answers):
            solving_task.answer = answer
            solving_task.save()

    def _set_earned_weight(self) -> None:
        self.earned_weight = 0
        for solving_task in self.solving_task_set.all():
            if solving_task.is_correctly_resolved():
                self.earned_weight += solving_task.task.weight

    def _set_assessment(self) -> None:
        self.assessment = round_up(self.earned_weight / self.testing.get_total_weight() * 5)

    def _set_end_passage(self) -> None:
        self.end_passage = datetime.now()

    def get_assessment_in_percentage(self) -> int:
        return round_up(self.earned_weight / self.testing.get_total_weight() * 100)

    class Meta(AbstractSolvingTesting.Meta):
        db_table = f'{APP_NAME}_solving-testing'
