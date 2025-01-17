from django.db import models

from apps.testing.constants import APP_NAME


class OpenQuestionAnswerOption(models.Model):
    RELATED_NAME = 'open_question_answer_option_set'

    correct_answer = models.CharField(verbose_name='Правильный ответ')
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Задача'
    )

    class Meta:
        db_table = f'{APP_NAME}_open-question-answer-option'
