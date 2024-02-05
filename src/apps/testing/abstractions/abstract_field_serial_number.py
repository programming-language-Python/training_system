from django.db import models


class AbstractFieldSerialNumber(models.Model):
    serial_number = models.IntegerField(
        blank=True,
        verbose_name='Порядковый номер'
    )

    class Meta:
        abstract = True
