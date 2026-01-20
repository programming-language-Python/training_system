from typing import Iterable, Mapping, Type

from apps.testing.abstractions.abstract_services import AbstractTaskWithChoiceService
from apps.testing.forms.solving_task_form import SolvingTaskWithChoiceForm, SolvingTaskWithRadioForm
from apps.testing.types import Id


class ClosedQuestionService(AbstractTaskWithChoiceService):
    @property
    def solving_form(self) -> Type[SolvingTaskWithChoiceForm] | Type[SolvingTaskWithRadioForm]:
        if self.task.closed_question_set.is_several_correct_answers:
            form = SolvingTaskWithChoiceForm
        else:
            form = SolvingTaskWithRadioForm
        return form

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
        closed_question_set = self.task.closed_question_set
        if closed_question_set.is_partially_correct_execution and closed_question_set.is_several_correct_answers:
            quantity_answers_coincidences = len(correct_answer_set & answer_set)
            quantity_correct_answers = len(correct_answer_set)
            quantity_answers_non_coincidences = len(answer_set - correct_answer_set)
            score = quantity_answers_coincidences / (quantity_correct_answers + quantity_answers_non_coincidences)
        elif closed_question_set.is_several_correct_answers:
            score = 1 if answer_set == correct_answer_set else 0
        else:
            score = 1 if answer in correct_answer_set else 0
        return score

    @property
    def _answer_options(self) -> Iterable:
        answer_option_set = self.task.answer_option_set
        if self.task.closed_question_set.is_random_order_answer_options:
            answer_options = answer_option_set.order_by('?')
        else:
            answer_options = answer_option_set.all()
        return answer_options
