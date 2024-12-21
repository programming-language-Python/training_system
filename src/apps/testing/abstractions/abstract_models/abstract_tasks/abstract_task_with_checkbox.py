from typing import Iterable

from django.db.models import QuerySet
from django.utils.html import strip_tags

from abstractions.abstract_models import AbstractTask
from apps.testing.types import Id, Description


class AbstractTaskWithCheckbox(AbstractTask):

    def get_initial_set_answer_options(self) -> Iterable[Id | Description]:
        set_answer_options = self.get_set_answer_options()
        ids = set_answer_options.values_list('id', flat=True)
        descriptions = map(strip_tags, set_answer_options.values_list('description', flat=True))
        return set(zip(ids, descriptions))

    def get_set_answer_options(self) -> QuerySet:
        raise NotImplementedError('Не реализован метод')

    class Meta(AbstractTask.Meta):
        abstract = True
