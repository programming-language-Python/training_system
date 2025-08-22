from datetime import timedelta, datetime

from django.db import models


class AbstractSolvingTesting(models.Model):
    RELATED_NAME = '%(app_label)s_solving_testing_set'

    assessment = models.IntegerField(null=True, verbose_name='Оценка')
    start_passage = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Начало прохождения'
    )
    end_passage = models.DateTimeField(
        null=True,
        default=None,
        verbose_name='Окончание прохождения'
    )
    testing = models.ForeignKey(
        'Testing',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Тестирование'
    )
    student = models.ForeignKey(
        'user.Student',
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Студент'
    )

    def __str__(self):
        return self.testing.title

    def get_solving_task_list_template(self) -> str:
        return f'{self._meta.app_label}/inc/solving_task/_solving_task_list.html'

    def is_testing_by_code(self) -> bool:
        return True if self._meta.app_label == 'testing_by_code' else False

    @property
    def duration(self) -> timedelta:
        return self.end_passage - datetime.now()

    def set_end_passage(self) -> None:
        if self.end_passage is None and self.testing.lead_time:
            lead_time = self.testing.lead_time
            lead_time_delta = timedelta(
                hours=lead_time.hour,
                minutes=lead_time.minute,
                seconds=lead_time.second,
                microseconds=lead_time.microsecond
            )
            self.end_passage = self.start_passage + lead_time_delta
            super(AbstractSolvingTesting, self).save()
        else:
            pass

    class Meta:
        abstract = True
        verbose_name = 'Решение тестирования'
        verbose_name_plural = 'Решения тестирований'
