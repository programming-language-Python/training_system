from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from abstractions.abstract_models import AbstractTask
from apps.testing.constants import APP_NAME
from apps.testing.types import TaskType
from config.settings import MAX_LENGTH


class Task(AbstractTask):
    TASKS_TYPES_CHOICES = [(type.value, _(type.value)) for type in TaskType]

    correct_answer = models.CharField(
        max_length=100,
        verbose_name='Правильный ответ'
    )
    type = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        choices=TASKS_TYPES_CHOICES,
        verbose_name='Тип'
    )
    testing = models.ForeignKey(
        'Testing',
        on_delete=models.CASCADE,
        verbose_name='Тестирование'
    )

    @property
    def additional_model(self) -> QuerySet | None:
        if self.type == TaskType.CLOSED_QUESTION:
            return self.closed_question_set
        else:
            return None

    @property
    def task_type(self) -> TaskType:
        return TaskType(self.type)

    @property
    def en_type(self) -> str:
        return self.task_type.en_value

    def get_absolute_url(self) -> reverse:
        kwargs = {'pk': self.pk}
        if self.testing.testing_solving_testing_set.exists():
            return reverse(f'{APP_NAME}:task_{self.en_type}_detail', kwargs=kwargs)
        else:
            return reverse(f'{APP_NAME}:task_{self.en_type}_update', kwargs=kwargs)

    def get_deletion_url(self) -> reverse:
        return reverse(f'{APP_NAME}:task_delete', kwargs={'pk': self.pk})
