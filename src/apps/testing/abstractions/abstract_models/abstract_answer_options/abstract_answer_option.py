from typing import Iterable

from django.db import models

from apps.testing.abstractions.abstract_fields import AbstractFieldSerialNumber, AbstractFieldDescription


class AbstractAnswerOption(AbstractFieldSerialNumber, AbstractFieldDescription):
    def get_fields(self) -> Iterable:
        exclude = ['id']
        exclude_types = (models.ForeignKey,)
        fields = []
        for field in self._meta.fields:
            if field.name not in exclude and not isinstance(field, exclude_types):
                fields.append(field)
        return fields

    class Meta:
        abstract = True
        ordering = ['serial_number', ]
