from typing import Iterable, Mapping

from apps.testing.abstractions.abstract_services import AbstractTaskWithChoiceService
from apps.testing.forms.solving_task_form import SolvingTaskWithChoiceForm, SolvingTaskWithRadioForm
from apps.testing.types import Id


class ClosedQuestionService(AbstractTaskWithChoiceService):

    def get_solving_form(self, solving_testing_pk: int):
        if self.task.closed_question_set.is_several_correct_answers:
            form = SolvingTaskWithChoiceForm
        else:
            form = SolvingTaskWithRadioForm
        form.base_fields['answer'].choices = self._get_answer_field_choices()
        return self.initialize_solving_form(form, solving_testing_pk)

    def update(self, cleaned_data: Mapping) -> None:
        closed_question = self.task.closed_question_set
        closed_question.is_several_correct_answers = cleaned_data['is_several_correct_answers']
        closed_question.is_random_order_answer_options = cleaned_data['is_random_order_answer_options']
        closed_question.is_partially_correct_execution = cleaned_data['is_partially_correct_execution']
        closed_question.save()

    def get_score(self, answer: Iterable[Id]) -> int | float:
        answer_options = self.task.answer_option_set
        correct_answer_set = set(map(str, answer_options.filter(is_correct=True).values_list('id', flat=True)))
        answer_set = set(answer)
        if self.task.closed_question_set.is_partially_correct_execution:
            quantity_answers_coincidences = len(correct_answer_set & answer_set)
            quantity_correct_answers = len(correct_answer_set)
            quantity_answers_non_coincidences = len(answer_set - correct_answer_set)
            score = quantity_answers_coincidences / (quantity_correct_answers + quantity_answers_non_coincidences)
        else:
            score = 1 if correct_answer_set == answer_set else 0
        return score

    @property
    def _answer_options(self) -> Iterable:
        answer_option_set = self.task.answer_option_set
        if self.task.closed_question_set.is_random_order_answer_options:
            answer_options = answer_option_set.order_by('?')
        else:
            answer_options = answer_option_set.all()
        return answer_options
