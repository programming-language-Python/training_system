from django.db import models
from django.urls import reverse

from apps.testing_by_code.constants import APP_NAME
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
        db_table = f'{APP_NAME}_operator_nesting'
        verbose_name = 'Вложенность оператора'
        verbose_name_plural = 'Вложенность операторов'
