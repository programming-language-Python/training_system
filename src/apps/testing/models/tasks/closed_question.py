from django.db import models

from abstractions.abstract_fields import AbstractFieldWeight
from apps.testing.abstractions import AbstractFieldText
from apps.testing.constants import APP_NAME


class ClosedQuestion(AbstractFieldText, AbstractFieldWeight):
    is_several_correct_answers = models.BooleanField(
        default=False,
        verbose_name='Несколько правильных ответов'
    )
    is_random_order_answer_options = models.BooleanField(
        default=False,
        verbose_name='Случайный порядок вариантов ответа'
    )
    is_partially_correct_execution = models.BooleanField(
        default=False,
        verbose_name='Учесть частично правильные выполнения задачи'
    )

    class Meta(AbstractFieldText.Meta, AbstractFieldWeight.Meta):
        pass


class AnswerOption(AbstractFieldText):
    is_correct = models.BooleanField(verbose_name='Правильный')
    closed_question = models.ForeignKey(
        ClosedQuestion,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Закрытый вопрос'
    )

    class Meta:
        db_table = f'{APP_NAME}_closedQuestion_answerOption'
