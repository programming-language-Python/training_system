from django.db import models

from abstractions.abstract_fields import AbstractFieldDescription, AbstractFieldSerialNumber


class AnswerOption(AbstractFieldSerialNumber, AbstractFieldDescription):
    RELATED_NAME = 'answer_option_set'

    is_correct = models.BooleanField(verbose_name='Правильный', default=False)
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Задача'
    )

    def get_fields(self):
        from apps.testing.services import get_model_fields
        return get_model_fields(
            model=self,
            excluded_fields=['id', 'task']
        )

    class Meta:
        ordering = ['serial_number', ]
