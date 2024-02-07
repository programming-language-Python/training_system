from django.db import models

from apps.testing.abstractions.abstract_fields import AbstractFieldDescription
from apps.testing.models import Testing


class EstablishingAccordance(AbstractFieldDescription):
    testing = models.ForeignKey(
        Testing,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Тестирование'
    )


class Answer(models.Model):
    pass
