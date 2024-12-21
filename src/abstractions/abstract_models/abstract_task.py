from typing import Iterable, Type

from django.db import models
from django.db.models import QuerySet
from django.forms import ModelForm
from django.urls import reverse

from apps.testing.abstractions.abstract_fields import AbstractFieldSerialNumber, AbstractFieldDescription
from apps.testing.abstractions.abstract_models.abstract_answer_options import AbstractAnswerOption
from apps.testing.constants import APP_NAME
from apps.testing.types import SolvingTask
from apps.testing.utils.conversion import convert_from_PascalCase_to_snake_case


class AbstractTask(AbstractFieldSerialNumber, AbstractFieldDescription):
    lead_time = models.TimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name='Время выполнения'
    )

    @staticmethod
    def get_solving_task_form() -> Type[ModelForm]:
        raise NotImplementedError('Не реализован метод get_solving_task_form')

    @staticmethod
    def get_or_create_solving_task(data) -> SolvingTask:
        raise NotImplementedError('Не реализован метод get_or_create_solving_task')

    def get_set_answer_options(self) -> QuerySet[AbstractAnswerOption]:
        raise NotImplementedError('Не реализован метод get_set_answer_options')

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def get_absolute_url(self) -> reverse:
        class_name = convert_from_PascalCase_to_snake_case(text=self.get_class_name())
        kwargs = {'pk': self.pk}
        if self.testing.testing_solving_testing_set.exists():
            return reverse(f'{APP_NAME}:task_{class_name}_detail', kwargs=kwargs)
        else:
            return reverse(f'{APP_NAME}:task_{class_name}_update', kwargs=kwargs)

    def get_deletion_url(self) -> reverse:
        class_name = convert_from_PascalCase_to_snake_case(text=self.get_class_name())
        return reverse(f'{APP_NAME}:task_{class_name}_delete', kwargs={'pk': self.pk})

    def get_fields(self) -> Iterable:
        exclude = ['id', 'serial_number', 'task_type', 'testing']
        field_values = []
        for field in self.__class__._meta.fields:
            if field.name not in exclude:
                if field.value_from_object(self):
                    if isinstance(field.value_from_object(self), bool):
                        field_values.append(f'{field.verbose_name}: да')
                    else:
                        field_values.append(f'{field.verbose_name}: {field.value_from_object(self)}')
                else:
                    field_values.append(f'{field.verbose_name}: нет')
        return field_values

    class Meta:
        abstract = True
        ordering = ['serial_number', ]
