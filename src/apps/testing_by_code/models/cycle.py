from django.db import models
from django.urls import reverse

from config.settings import MAX_LENGTH


class Cycle(models.Model):
    title = models.CharField(max_length=MAX_LENGTH, verbose_name='Цикл')

    def get_absolute_url(self):
        return reverse('cycle_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Цикл'
        verbose_name_plural = 'Циклы'
