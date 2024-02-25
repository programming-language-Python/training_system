from django.db import models

from apps.testing.abstractions.abstract_models.abstract_answer_options import AbstractOpenQuestionAnswerOption
from apps.testing.abstractions.abstract_models.abstract_tasks import AbstractOpenQuestion
from apps.testing.constants import APP_NAME
from apps.testing.models.completed_testing import CompletedTesting


class CompletedOpenQuestion(AbstractOpenQuestion):
    student_answer = models.CharField(verbose_name='Ответ студента')
    completed_testing = models.ForeignKey(
        CompletedTesting,
        on_delete=models.CASCADE,
        related_name='completed_open_question_set',
        verbose_name='Завершённое тестирование'
    )

    class Meta:
        db_table = f'{APP_NAME}_completedOpenQuestion'


class OpenQuestionAnswerOptionCorrect(AbstractOpenQuestionAnswerOption):
    completed_open_question = models.ForeignKey(
        CompletedOpenQuestion,
        on_delete=models.CASCADE,
        related_name='completed_open_question_answer_option_set',
        verbose_name='Завершённый открытый вопрос'
    )

    class Meta:
        db_table = f'{APP_NAME}_openQuestion_answerOption_correct'
