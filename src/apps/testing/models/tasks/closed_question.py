from django.db import models

from apps.testing.abstractions.abstract_models.abstract_answer_options import AbstractClosedQuestionAnswerOption
from apps.testing.abstractions.abstract_models.abstract_tasks import AbstractClosedQuestion
from apps.testing.constants import APP_NAME
from apps.testing.models import Testing


class ClosedQuestion(AbstractClosedQuestion):
    testing = models.ForeignKey(
        Testing,
        on_delete=models.CASCADE,
        related_name='closed_question_set',
        verbose_name='Тестирование'
    )


class ClosedQuestionAnswerOption(AbstractClosedQuestionAnswerOption):
    closed_question = models.ForeignKey(
        ClosedQuestion,
        on_delete=models.CASCADE,
        related_name='closed_question_answer_option_set',
        verbose_name='Закрытый вопрос'
    )

    class Meta(AbstractClosedQuestionAnswerOption.Meta):
        db_table = f'{APP_NAME}_closedQuestion_answerOption'
