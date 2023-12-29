from django.db import models

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

    class Meta:
        abstract = True
        verbose_name = 'Тестирование'
        verbose_name_plural = 'Тестирования'
