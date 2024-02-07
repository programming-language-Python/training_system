from apps.testing.abstractions.abstract_fields import AbstractFieldSerialNumber, AbstractFieldDescription


class AbstractTask(AbstractFieldSerialNumber, AbstractFieldDescription):
    def get_class_name(self) -> str:
        return self.__class__.__name__

    class Meta:
        abstract = True
