from typing import Iterable, Type

from apps.testing.abstractions.abstract_services import AbstractTaskWithChoiceService
from apps.testing.forms.solving_task_form import SolvingSequencingForm
from apps.testing.types import Id


class SequencingService(AbstractTaskWithChoiceService):
    @property
    def solving_form(self) -> Type[SolvingSequencingForm]:
        return SolvingSequencingForm

    def get_score(self, answer: Iterable[Id]) -> int:
        user_answer = list(map(int, answer))
        correct_answers = list(
            self.task.answer_option_set.filter(
                is_correct=True
            ).values_list('id', flat=True)
        )
        return 1 if user_answer == correct_answers else 0

    @property
    def _answer_options(self) -> Iterable:
        return self.task.answer_option_set.order_by('?')
