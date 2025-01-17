from typing import Iterable

from django.db import models
from django.urls import reverse

from abstractions.abstract_fields import AbstractFieldSerialNumber, AbstractFieldDescription
from services import get_field_values


class AbstractTask(AbstractFieldSerialNumber, AbstractFieldDescription):
    lead_time = models.TimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name='Время выполнения'
    )

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def get_absolute_url(self) -> reverse:
        raise NotImplementedError('Не реализован метод get_absolute_url')

    def get_fields(self) -> Iterable:
        return get_field_values(
            model=self,
            excluded_fields=['id', 'serial_number', 'type', 'testing']
        )

    class Meta:
        abstract = True
        ordering = ['serial_number', ]
