from django.db import models


class AbstractFieldWeight(models.Model):
    weight = models.IntegerField(default=1, verbose_name='Вес')

    class Meta:
        abstract = True
