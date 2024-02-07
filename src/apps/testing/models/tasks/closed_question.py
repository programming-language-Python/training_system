from django.db import models
from django.urls import reverse

from apps.testing.abstractions.abstract_models import AbstractTask
from apps.testing.constants import APP_NAME
from apps.testing.models import Testing


class ClosedQuestion(AbstractTask):
    type = models.CharField(default='Закрытый вопрос')
    is_several_correct_answers = models.BooleanField(
        default=False,
        verbose_name='Допустимо несколько правильных ответов'
    )
    is_random_order_answer_options = models.BooleanField(
        default=False,
        verbose_name='Случайный порядок вариантов ответа'
    )
    is_partially_correct_execution = models.BooleanField(
        default=False,
        verbose_name='При оценке учесть частично правильное выполнение задания'
    )
    testing = models.ForeignKey(
        Testing,
        on_delete=models.CASCADE,
        related_name='closed_question_set',
        verbose_name='Тестирование'
    )

    def get_absolute_url(self):
        return reverse(APP_NAME + ':task_closed_question_update', kwargs={'pk': self.pk})

    def get_deletion_url(self):
        return reverse(APP_NAME + ':task_closed_question_delete', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['serial_number', ]


class ClosedQuestionAnswerOption(AbstractTask):
    is_correct = models.BooleanField(verbose_name='Правильный')
    closed_question = models.ForeignKey(
        ClosedQuestion,
        on_delete=models.CASCADE,
        related_name='closed_question_answer_option_set',
        verbose_name='Закрытый вопрос'
    )

    class Meta:
        ordering = ['serial_number', ]
        db_table = f'{APP_NAME}_closedQuestion_answerOption'
