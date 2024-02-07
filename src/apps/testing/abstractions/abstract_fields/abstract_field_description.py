from django.db import models


class AbstractFieldDescription(models.Model):
    description = models.TextField(verbose_name='Описание')

    class Meta:
        abstract = True
