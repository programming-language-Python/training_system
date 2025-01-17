from typing import Mapping

from django.db import models
from django.db.models import OneToOneRel, ManyToManyRel, ManyToOneRel

from abstractions.abstract_fields import AbstractFieldTitle
from apps.user.models import StudentGroup, Teacher


class AbstractTesting(AbstractFieldTitle):
    RELATED_NAME = '%(app_label)s_%(class)s_set'

    is_published = models.BooleanField(
        blank=True,
        default=False,
        verbose_name='Опубликовано'
    )
    is_review_of_result_by_student = models.BooleanField(
        blank=True,
        default=True,
        verbose_name='Просмотр результата студентом'
    )
    is_established_order_tasks = models.BooleanField(
        verbose_name='Установленный порядок задач',
        default=False
    )
    date_of_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    date_of_deletion = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Дата удаления'
    )
    task_lead_time = models.TimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Время выполнения задачи'
    )
    student_groups = models.ManyToManyField(
        StudentGroup,
        blank=True,
        related_name=RELATED_NAME,
        verbose_name='Группы студентов'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name=RELATED_NAME,
        verbose_name='Преподаватель'
    )

    def __str__(self):
        return self.title

    def get_task_lead_time(self):
        return self.task_lead_time

    def get_fields_data(self) -> Mapping[str, str]:
        exclude = ['id', 'teacher', 'date_of_deletion', 'max_score', ]
        exclude_types = (OneToOneRel, ManyToOneRel, ManyToManyRel)
        fields_data = {}
        for field in self._meta.get_fields():
            is_boolean_field = isinstance(field, models.BooleanField)
            if is_boolean_field:
                fields_data[field.verbose_name] = 'да' if field.value_to_string(self) == 'True' else 'нет'
                continue
            is_empty_task_lead_time = field.name == 'task_lead_time' and not field.value_to_string(self)
            if is_empty_task_lead_time:
                fields_data[field.verbose_name] = 'не задано'
                continue
            if field.name == 'student_groups':
                fields_data[field.verbose_name] = self.student_groups.values('name')
            elif field.name not in exclude and not isinstance(field, exclude_types):
                fields_data[field.verbose_name] = field.value_to_string(self)
        return fields_data

    class Meta:
        abstract = True
        verbose_name = 'Тестирование'
        verbose_name_plural = 'Тестирования'
