from django.db import models

from abstractions.abstract_models.abstract_completed_testing import AbstractCompletedTesting


class CompletedTesting(AbstractCompletedTesting):
    start_passage = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Начало прохождения'
    )
    end_passage = models.DateTimeField(
        null=True,
        verbose_name='Окончание прохождения'
    )

    class Meta:
        db_table = 'testing_сompletedTesting'
