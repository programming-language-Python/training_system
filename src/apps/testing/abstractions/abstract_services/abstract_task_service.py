from typing import Type

from apps.testing.forms.solving_task_form import SolvingTaskForm


class AbstractTaskService:
    def __init__(self, task):
        self.task = task

    @property
    def solving_form(self) -> Type[SolvingTaskForm]:
        raise NotImplementedError('Не реализован метод solving_form')

    def initialize_solving_form(self, solving_testing_pk: int) -> Type[SolvingTaskForm]:
        raise NotImplementedError('Не реализован метод initialize_solving_form')
