import datetime
from typing import Iterable

from django.db import models


class AbstractSolvingTask(models.Model):
    answer = models.CharField(blank=True, max_length=100, verbose_name='Ответ')
    start_passage = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Начало прохождения'
    )
    end_passage = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Конец прохождения'
    )
    lead_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Время выполнения'
    )

    def get_fields(self) -> Iterable:
        exclude = ['id', 'task', 'solving_testing', 'answer']
        field_values = []
        for field in self.__class__._meta.fields:
            if field.name not in exclude:
                field_values.append(f'{field.verbose_name}: {field.value_from_object(self)}')
        return field_values

    def set_start_passage(self):
        if not self.start_passage:
            self.start_passage = datetime.datetime.now()
            self.save()

    class Meta:
        abstract = True
