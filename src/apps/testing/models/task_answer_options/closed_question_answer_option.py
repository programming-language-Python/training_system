from django.db import models

from apps.testing.abstractions.abstract_models.abstract_answer_options import AbstractAnswerOption
from apps.testing.constants import APP_NAME
from apps.testing.models.tasks import ClosedQuestion


class ClosedQuestionAnswerOption(AbstractAnswerOption):
    is_correct = models.BooleanField(verbose_name='Правильный')
    closed_question = models.ForeignKey(
        ClosedQuestion,
        on_delete=models.CASCADE,
        related_name='closed_question_answer_option_set',
        verbose_name='Закрытый вопрос'
    )

    class Meta(AbstractAnswerOption.Meta):
        db_table = f'{APP_NAME}_closed-question-answer-option'
