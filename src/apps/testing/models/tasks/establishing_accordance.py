from django.db import models

from abstractions.abstract_fields import AbstractFieldWeight
from apps.testing.abstractions import AbstractFieldText


class EstablishingAccordance(AbstractFieldText, AbstractFieldWeight):
    pass


class Answer(models.Model):
    pass
