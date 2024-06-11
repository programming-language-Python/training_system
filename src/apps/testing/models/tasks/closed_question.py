from typing import Iterable, Type

from django.db import models
from django.forms import ModelForm
from django.utils.html import strip_tags

from abstractions.abstract_models import AbstractTask
from apps.testing.constants import APP_NAME
from apps.testing.models import Testing
from apps.testing.models.solving_tasks import SolvingClosedQuestion
from apps.testing.models.tasks import TaskType
from apps.testing.types import Id, Description, SolvingTask


class ClosedQuestion(AbstractTask):
    RELATED_NAME = 'closed_question_set'

    is_several_correct_answers = models.BooleanField(
        default=False,
        verbose_name='Допустимо несколько правильных ответов'
    )
    is_random_order_answer_options = models.BooleanField(
        default=False,
        verbose_name='Случайный порядок вариантов ответа'
    )
    is_partially_correct_execution = models.BooleanField(
        default=False,
        verbose_name='При оценке учесть частично правильное выполнение задания'
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Тип задачи'
    )
    testing = models.ForeignKey(
        Testing,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Тестирование'
    )

    @staticmethod
    def get_solving_task_form() -> Type[ModelForm]:
        from apps.testing.forms.task_forms.сlosed_question_form import SolvingClosedQuestionForm
        return SolvingClosedQuestionForm

    @staticmethod
    def get_or_create_solving_task(data) -> SolvingTask:
        solving_task, _ = SolvingClosedQuestion.objects.get_or_create(**data)
        return solving_task

    def get_weight(self, answer: Iterable[Id]) -> int:
        answer_options = self.closed_question_answer_option_set
        quantity_correct_answers = answer_options.filter(
            is_correct=True
        ).count()
        quantity_correct_user_answers = answer_options.filter(
            id__in=answer,
            is_correct=True
        ).count()
        return 1 if quantity_correct_answers == quantity_correct_user_answers else 0

    def get_set_answer_options(self) -> Iterable[Id | Description]:
        if self.is_random_order_answer_options:
            all_answer_options = self.closed_question_answer_option_set.order_by('?')
        else:
            all_answer_options = self.closed_question_answer_option_set.all()
        ids = all_answer_options.values_list('id', flat=True)
        descriptions = map(strip_tags, all_answer_options.values_list('description', flat=True))
        return set(zip(ids, descriptions))

    class Meta(AbstractTask.Meta):
        db_table = f'{APP_NAME}_closed-question'
