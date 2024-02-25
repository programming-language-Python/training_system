from django.db import models

from apps.testing.abstractions.abstract_models.abstract_tasks import AbstractTask


class AbstractOpenQuestion(AbstractTask):
    type = models.CharField(default='Открытый вопрос')

    class Meta:
        abstract = True
