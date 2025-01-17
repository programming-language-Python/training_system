from typing import Iterable, Mapping

from apps.testing.models import Task, SolvingTask
from apps.testing.types import Id


def closed_question_set_answer(solving_task: SolvingTask, answer: Iterable[Id]) -> None:
    solving_task.answer = ', '.join(answer)
    solving_task.save()


class ClosedQuestionService:
    task: Task

    def __init__(self, task: Task):
        self.task = task

    def get_answer_options(self) -> Iterable:
        answer_option_set = self.task.answer_option_set
        if self.task.closed_question_set.is_random_order_answer_options:
            answer_options = answer_option_set.order_by('?')
        else:
            answer_options = answer_option_set.all()
        return answer_options

    def update(self, cleaned_data: Mapping) -> None:
        closed_question = self.task.closed_question_set
        closed_question.is_several_correct_answers = cleaned_data['is_several_correct_answers']
        closed_question.is_random_order_answer_options = cleaned_data['is_random_order_answer_options']
        closed_question.is_partially_correct_execution = cleaned_data['is_partially_correct_execution']
        closed_question.save()

    def get_weight(self, answer: Iterable[Id]) -> int:
        answer_options = self.task.answer_option_set
        quantity_correct_answers = answer_options.filter(
            is_correct=True
        ).count()
        quantity_correct_user_answers = answer_options.filter(
            id__in=answer,
            is_correct=True
        ).count()
        return 1 if quantity_correct_answers == quantity_correct_user_answers else 0
