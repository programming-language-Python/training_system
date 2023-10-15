from django.db import models


class AbstractFieldText(models.Model):
    text = models.TextField(verbose_name='Текст задания')

    class Meta:
        abstract = True
