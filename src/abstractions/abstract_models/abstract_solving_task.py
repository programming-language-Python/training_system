from django.db import models


class AbstractSolvingTask(models.Model):
    answer = models.CharField(max_length=100, verbose_name='Ответ')
    start_passage = models.DateTimeField(verbose_name='Начало прохождения')
    lead_time = models.TimeField(verbose_name='Время выполнения')

    class Meta:
        abstract = True
