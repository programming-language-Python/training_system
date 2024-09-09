from datetime import timedelta, datetime
from typing import Iterable, Sequence, Mapping

from django.db import models

from apps.testing.types import Id, SolvingTask
from apps.testing_by_code.utils.utils import round_up


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

    def get_duration(self) -> timedelta:
        return self.end_passage - datetime.now()

    def is_time_up(self) -> bool:
        return self.end_passage <= datetime.now()

    def set_end_passage(self, quantity_tasks: int) -> None:
        if self.end_passage is None:
            task_lead_time = self.testing.task_lead_time
            time_delta = timedelta(
                hours=task_lead_time.hour,
                minutes=task_lead_time.minute,
                seconds=task_lead_time.second
            )
            duration = time_delta * quantity_tasks
            self.end_passage = self.start_passage + duration
            super(AbstractSolvingTesting, self).save()

    def save(self, *args, **kwargs: Mapping[str, Sequence[SolvingTask]]) -> None:
        task_forms = kwargs.get('task_forms')
        if task_forms:
            self.end_passage = datetime.now()
            self.assessment = self._get_assessment(task_forms)
        super(AbstractSolvingTesting, self).save()

    @staticmethod
    def _get_assessment(task_forms: Sequence[SolvingTask]) -> float:
        answer: str | Iterable[Id]
        weight = 0
        for task_form in task_forms:
            task = task_form.initial['solving_task'].task
            answer = task_form.cleaned_data['answer']
            weight += task.get_weight(answer)
        assessment = round_up(weight / len(task_forms) * 5)
        return assessment

    class Meta:
        abstract = True
        verbose_name = 'Решение тестирования'
        verbose_name_plural = 'Решения тестирований'
