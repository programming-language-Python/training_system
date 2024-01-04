from typing import Mapping

from django.db import models
from django.db.models import OneToOneRel, ManyToManyRel, ManyToOneRel

from abstractions.abstract_fields import AbstractFieldTitle
from apps.user.models import StudentGroup, User


class AbstractTesting(AbstractFieldTitle):
    is_published = models.BooleanField(
        blank=True,
        default=True,
        verbose_name='Опубликовано'
    )
    is_review_of_result_by_student = models.BooleanField(
        blank=True,
        default=True,
        verbose_name='Просмотр результата студентом'
    )
    student_groups = models.ManyToManyField(
        StudentGroup,
        blank=True,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Группы студентов'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Пользователь'
    )

    def __str__(self):
        return self.title

    def get_fields_data(self) -> Mapping[str, str]:
        exclude = ['id', 'user']
        exclude_types = (OneToOneRel, ManyToOneRel, ManyToManyRel)
        fields_data = {}
        for field in self._meta.get_fields():
            if isinstance(field, models.BooleanField):
                fields_data[field.verbose_name] = 'да' if field.value_to_string(self) == 'True' else 'нет'
                continue
            if field.name == 'student_groups':
                fields_data[field.verbose_name] = self.student_groups.values('title')
            elif field.name not in exclude and not isinstance(field, exclude_types):
                fields_data[field.verbose_name] = field.value_to_string(self)
        return fields_data

    class Meta:
        abstract = True
        verbose_name = 'Тестирование'
        verbose_name_plural = 'Тестирования'
