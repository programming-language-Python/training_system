from apps.testing.abstractions.abstract_fields import AbstractFieldSerialNumber, AbstractFieldDescription


class AbstractAnswerOption(AbstractFieldSerialNumber, AbstractFieldDescription):
    class Meta:
        abstract = True
        ordering = ['serial_number', ]
