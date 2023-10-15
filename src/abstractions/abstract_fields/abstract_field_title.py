from django.db import models

from config.settings import MAX_LENGTH


class AbstractFieldTitle(models.Model):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Наименование',
        unique=True
    )

    class Meta:
        abstract = True
