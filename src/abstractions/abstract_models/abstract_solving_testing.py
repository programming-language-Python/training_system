from django.db import models

from abstractions.abstract_fields import AbstractFieldTitle


class AbstractSolvingTesting(AbstractFieldTitle):
    RELATED_NAME = '%(app_label)s_solving_testing_set'

    assessment = models.IntegerField(null=True, verbose_name='Оценка')
    start_passage = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Начало прохождения'
    )
    end_passage = models.DateTimeField(
        null=True,
        default=None,
        verbose_name='Окончание прохождения'
    )
    testing = models.ForeignKey(
        'Testing',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Тестирование'
    )
    student = models.ForeignKey(
        'user.Student',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Студент'
    )

    class Meta:
        abstract = True
        verbose_name = 'Решение тестирования'
        verbose_name_plural = 'Решения тестирований'
