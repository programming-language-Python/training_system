from django.db import models
from django.db.models import QuerySet, Case, When, BooleanField, Value

from abstractions.abstract_models import AbstractSolvingTask
from apps.testing.constants import APP_NAME
from apps.testing.types import TaskType


class SolvingTask(AbstractSolvingTask):
    RELATED_NAME = 'solving_task_set'

    answer = models.JSONField(null=True, blank=True, verbose_name='Ответ')
    score = models.FloatField(default=0.0, verbose_name='Балл')
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Задача'
    )
    solving_testing = models.ForeignKey(
        'SolvingTesting',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Решение тестирования'
    )

    @property
    def selected_answer_options_template(self) -> str:
        return f'testing/inc/selected_answer_options/_selected_answer_options_{self.task.en_type}.html'

    @property
    def selected_answer_options(self) -> str | QuerySet:
        task = self.task
        match task.type:
            case TaskType.CLOSED_QUESTION:
                return task.answer_option_set.all().annotate(
                    is_selected=Case(
                        When(id__in=self.answer, then=Value(True)),
                        default=Value(False),
                        output_field=BooleanField()
                    )
                )
            case TaskType.SEQUENCING:
                preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(self.answer)])
                return task.answer_option_set.filter(pk__in=self.answer).order_by(preserved)
            case TaskType.OPEN_QUESTION:
                return self.answer

    class Meta:
        db_table = f'{APP_NAME}_solving-task'
        ordering = ('task__serial_number',)
