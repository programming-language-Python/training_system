from django.db import models

from apps.testing.abstractions.abstract_models.abstract_answer_options import AbstractOpenQuestionAnswerOption
from apps.testing.abstractions.abstract_models.abstract_tasks import AbstractOpenQuestion
from apps.testing.constants import APP_NAME
from apps.testing.models import Testing


class OpenQuestion(AbstractOpenQuestion):
    testing = models.ForeignKey(
        Testing,
        on_delete=models.CASCADE,
        related_name='open_question_set',
        verbose_name='Тестирование'
    )


class OpenQuestionAnswerOption(AbstractOpenQuestionAnswerOption):
    open_question = models.ForeignKey(
        OpenQuestion,
        on_delete=models.CASCADE,
        related_name='open_question_answer_option_set',
        verbose_name='Открытый вопрос'
    )

    class Meta:
        db_table = f'{APP_NAME}_openQuestion_answerOption'
