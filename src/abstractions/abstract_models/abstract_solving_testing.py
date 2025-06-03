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

    def get_end_passage(self) -> datetime:
        return self.end_passage

    def get_duration(self) -> timedelta:
        return self.end_passage - datetime.now()

    def is_time_up(self) -> bool:
        if self.end_passage is None:
            return False
        else:
            return self.end_passage <= datetime.now()

    def set_end_passage(self, quantity_tasks: int) -> None:
        task_lead_time = self.testing.get_task_lead_time()
        is_task_lead_time = task_lead_time is not None
        if self.end_passage is None and is_task_lead_time:
            time_delta = timedelta(
                hours=task_lead_time.hour,
                minutes=task_lead_time.minute,
                seconds=task_lead_time.second
            )
            duration = time_delta * quantity_tasks
            self.end_passage = self.start_passage + duration
            super(AbstractSolvingTesting, self).save()
        else:
            pass

    def get_end_passage_iso_format(self) -> str:
        if self.end_passage is None:
            return ''
        return self.end_passage.isoformat()

    class Meta:
        abstract = True
        verbose_name = 'Решение тестирования'
        verbose_name_plural = 'Решения тестирований'
