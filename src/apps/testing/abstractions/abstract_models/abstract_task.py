from django.urls import reverse

from apps.testing.abstractions.abstract_fields import AbstractFieldSerialNumber, AbstractFieldDescription
from apps.testing.constants import APP_NAME
from apps.testing.utils.text import convert_from_PascalCase_to_snake_case


class AbstractTask(AbstractFieldSerialNumber, AbstractFieldDescription):
    def get_class_name(self) -> str:
        return self.__class__.__name__

    def get_absolute_url(self):
        class_name = convert_from_PascalCase_to_snake_case(text=self.get_class_name())
        return reverse(f'{APP_NAME}:task_{class_name}_update', kwargs={'pk': self.pk})

    def get_deletion_url(self):
        class_name = convert_from_PascalCase_to_snake_case(text=self.get_class_name())
        return reverse(f'{APP_NAME}:task_{class_name}_delete', kwargs={'pk': self.pk})

    class Meta:
        abstract = True
        ordering = ['serial_number', ]
