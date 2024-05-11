import datetime

from django.db import models


class AbstractSolvingTask(models.Model):
    answer = models.CharField(blank=True, max_length=100, verbose_name='Ответ')
    start_passage = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Начало прохождения'
    )
    lead_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Время выполнения'
    )

    def set_start_passage(self):
        if not self.start_passage:
            self.start_passage = datetime.datetime.now()
            self.save()

    class Meta:
        abstract = True
