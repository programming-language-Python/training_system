from typing import Iterable, Mapping

from apps.testing.abstractions.abstract_services import AbstractTaskWithChoiceService
from apps.testing.forms.solving_task_form import SolvingTaskWithChoiceForm
from apps.testing.types import Id


class ClosedQuestionService(AbstractTaskWithChoiceService):

    def get_solving_form(self, solving_testing_pk: int):
        form = SolvingTaskWithChoiceForm
        form.base_fields['answer'].choices = self._get_answer_field_choices()
        return self.initialize_solving_form(form, solving_testing_pk)

    def update(self, cleaned_data: Mapping) -> None:
        closed_question = self.task.closed_question_set
        closed_question.is_several_correct_answers = cleaned_data['is_several_correct_answers']
        closed_question.is_random_order_answer_options = cleaned_data['is_random_order_answer_options']
        closed_question.is_partially_correct_execution = cleaned_data['is_partially_correct_execution']
        closed_question.save()

    def get_score(self, answer: Iterable[Id]) -> int:
        answer_options = self.task.answer_option_set
        quantity_correct_answers = answer_options.filter(
            is_correct=True
        ).count()
        quantity_correct_user_answers = answer_options.filter(
            id__in=answer,
            is_correct=True
        ).count()
        return 1 if quantity_correct_answers == quantity_correct_user_answers else 0

    @property
    def _answer_options(self) -> Iterable:
        answer_option_set = self.task.answer_option_set
        if self.task.closed_question_set.is_random_order_answer_options:
            answer_options = answer_option_set.order_by('?')
        else:
            answer_options = answer_option_set.all()
        return answer_options
