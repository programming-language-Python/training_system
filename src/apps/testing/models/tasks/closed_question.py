from django.db import models

from abstractions.abstract_fields import AbstractFieldWeight
from apps.testing.abstractions.abstract_field_description import AbstractFieldDescription
from apps.testing.constants import APP_NAME
from apps.testing.models import Testing


class ClosedQuestion(AbstractFieldDescription, AbstractFieldWeight):
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
    testing = models.ForeignKey(
        Testing,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Тестирование'
    )

    class Meta(AbstractFieldDescription.Meta, AbstractFieldWeight.Meta):
        pass


class AnswerOption(AbstractFieldDescription):
    is_correct = models.BooleanField(verbose_name='Правильный')
    closed_question = models.ForeignKey(
        ClosedQuestion,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Закрытый вопрос'
    )

    class Meta:
        db_table = f'{APP_NAME}_closedQuestion_answerOption'
