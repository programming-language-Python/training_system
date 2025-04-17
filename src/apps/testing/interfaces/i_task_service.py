from typing import Protocol, Iterable, Type

from django.forms import ModelForm

from apps.testing.types import Id


class ITaskService(Protocol):
    def get_weight(self, answer: Iterable[Id] | str) -> int:
        raise NotImplementedError

    @property
    def solving_form(self) -> Type[ModelForm]:
        raise NotImplementedError
