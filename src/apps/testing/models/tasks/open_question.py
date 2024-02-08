from django.db import models

from apps.testing.abstractions.abstract_models import AbstractTask
from apps.testing.constants import APP_NAME
from apps.testing.models import Testing


class OpenQuestion(AbstractTask):
    type = models.CharField(default='Открытый вопрос')
    testing = models.ForeignKey(
        Testing,
        on_delete=models.CASCADE,
        related_name='open_question_set',
        verbose_name='Тестирование'
    )


class OpenQuestionAnswerOption(models.Model):
    correct_answer = models.CharField(verbose_name='Правильный ответ')
    open_question = models.ForeignKey(
        OpenQuestion,
        on_delete=models.CASCADE,
        related_name='open_question_answer_option_set',
        verbose_name='Открытый вопрос'
    )

    class Meta:
        db_table = f'{APP_NAME}_openQuestion_answerOption'
