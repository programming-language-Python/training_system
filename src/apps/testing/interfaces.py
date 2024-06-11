from typing import Protocol, Type

from django.forms import ModelForm

from apps.testing.types import SolvingTask


class ITask(Protocol):
    @staticmethod
    def get_solving_task_form() -> Type[ModelForm]:
        raise NotImplementedError

    @staticmethod
    def get_or_create_solving_task(data) -> SolvingTask:
        raise NotImplementedError
