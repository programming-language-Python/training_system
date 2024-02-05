from apps.testing.abstractions import AbstractFieldDescription, AbstractFieldSerialNumber


class AbstractTask(AbstractFieldSerialNumber, AbstractFieldDescription):
    def get_class_name(self) -> str:
        return self.__class__.__name__

    class Meta:
        abstract = True
