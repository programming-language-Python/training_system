from typing import Iterable

from django.db import models


class AbstractSolvingTask(models.Model):
    answer = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Ответ'
    )
    time_left = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Оставшееся время'
    )

    def get_fields(self) -> Iterable:
        exclude = ['id', 'task', 'solving_testing', 'answer']
        field_values = []
        for field in self.__class__._meta.fields:
            if field.name not in exclude:
                field_values.append(f'{field.verbose_name}: {field.value_from_object(self)}')
        return field_values

    class Meta:
        abstract = True
