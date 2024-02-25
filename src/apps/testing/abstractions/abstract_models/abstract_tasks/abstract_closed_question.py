from django.db import models

from apps.testing.abstractions.abstract_models.abstract_tasks import AbstractTask


class AbstractClosedQuestion(AbstractTask):
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

    class Meta:
        abstract = True
