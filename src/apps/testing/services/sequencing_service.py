from typing import Iterable

from apps.testing.abstractions.abstract_services import AbstractTaskWithChoiceService
from apps.testing.forms.solving_task_form import SolvingSequencingForm
from apps.testing.types import Id


class SequencingService(AbstractTaskWithChoiceService):
    def get_solving_form(self, solving_testing_pk: int):
        form = SolvingSequencingForm
        form.base_fields['answer'].choices = self._get_answer_field_choices()
        return self.initialize_solving_form(form, solving_testing_pk)

    def get_weight(self, answer: Iterable[Id]) -> int:
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
