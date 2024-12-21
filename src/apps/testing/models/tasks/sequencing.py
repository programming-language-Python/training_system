from typing import Type

from django.db import models
from django.db.models import QuerySet
from django.forms import ModelForm

from apps.testing.abstractions.abstract_models.abstract_tasks import AbstractTaskWithCheckbox
from apps.testing.models import Testing
from apps.testing.models.solving_tasks import SolvingSequencing
from apps.testing.models.tasks import TaskType
from apps.testing.types import SolvingTask


class Sequencing(AbstractTaskWithCheckbox):
    RELATED_NAME = 'sequencing_set'

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
        solving_task, _ = SolvingSequencing.objects.get_or_create(**data)
        return solving_task

    def get_set_answer_options(self) -> QuerySet:
        return self.sequencing_answer_option_set.order_by('?')

    class Meta(AbstractTaskWithCheckbox.Meta):
        pass
