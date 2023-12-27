from django.db import models

from abstractions.abstract_fields import AbstractFieldWeight
from apps.testing.abstractions.abstract_field_description import AbstractFieldDescription
from apps.testing.models import Testing


class EstablishingAccordance(AbstractFieldDescription, AbstractFieldWeight):
    testing = models.ForeignKey(
        Testing,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Тестирование'
    )


class Answer(models.Model):
    pass
