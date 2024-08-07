from django.db import models

from apps.testing.abstractions.abstract_models.abstract_answer_options import AbstractAnswerOption
from apps.testing.constants import APP_NAME
from apps.testing.models.tasks import OpenQuestion


class OpenQuestionAnswerOption(AbstractAnswerOption):
    serial_number = None
    description = None

    correct_answer = models.CharField(verbose_name='Правильный ответ')
    open_question = models.ForeignKey(
        OpenQuestion,
        on_delete=models.CASCADE,
        related_name='open_question_answer_option_set',
        verbose_name='Открытый вопрос'
    )

    class Meta:
        db_table = f'{APP_NAME}_open-question-answer-option'
