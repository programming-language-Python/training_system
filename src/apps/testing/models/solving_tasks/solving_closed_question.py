from django.db import models
from django.db.models import QuerySet, Case, When, Value, BooleanField

from abstractions.abstract_models import AbstractSolvingTask
from apps.testing.constants import APP_NAME
from apps.testing.models import SolvingTesting


class SolvingClosedQuestion(AbstractSolvingTask):
    RELATED_NAME = 'solving_closed_question_set'

    task = models.ForeignKey(
        'ClosedQuestion',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Закрытый вопрос'
    )
    solving_testing = models.ForeignKey(
        SolvingTesting,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Решение тестирования'
    )

    def get_selected_answer_options(self) -> QuerySet:
        return self.task.closed_question_answer_option_set.all().annotate(
            is_selected=Case(
                When(id__in=self.answer.split(', '), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

    def set_answer(self, answer) -> None:
        self.answer = ', '.join(answer)
        self.save()

    class Meta:
        db_table = f'{APP_NAME}_solving-closed-question'
