from typing import Type

from django.db import models
from django.db.models import QuerySet
from django.forms import ModelForm

from abstractions.abstract_models import AbstractTask
from apps.testing.constants import APP_NAME
from apps.testing.models import Testing
from apps.testing.models.solving_tasks import SolvingOpenQuestion
from apps.testing.models.tasks import TaskType


class OpenQuestion(AbstractTask):
    RELATED_NAME = 'open_question_set'

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

    def get_set_answer_options(self) -> QuerySet:
        return self.open_question_answer_option_set.all()

    @staticmethod
    def get_solving_task_form() -> Type[ModelForm]:
        from apps.testing.forms.task_forms.open_question_form import SolvingOpenQuestionForm
        return SolvingOpenQuestionForm

    @staticmethod
    def get_or_create_solving_task(data) -> SolvingOpenQuestion:
        solving_task, _ = SolvingOpenQuestion.objects.get_or_create(**data)
        return solving_task

    def get_weight(self, answer: str) -> int:
        is_correct_answer = self.open_question_answer_option_set.filter(
            correct_answer=answer
        ).exists()
        return 1 if is_correct_answer else 0

    class Meta(AbstractTask.Meta):
        db_table = f'{APP_NAME}_open-question'
