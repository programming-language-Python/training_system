from django.db import models
from django.urls import reverse

from config.settings import MAX_LENGTH


class OperatorNesting(models.Model):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Вложенность операторов'
    )

    def get_absolute_url(self):
        return reverse('operator_nesting_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вложенность оператора'
        verbose_name_plural = 'Вложенность операторов'
