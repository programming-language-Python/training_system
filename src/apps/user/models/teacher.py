from django.db import models

from apps.user.models import StudentGroup
from config.settings import AUTH_USER_MODEL


class Teacher(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Преподаватель'
    )
    teacher_group = models.ForeignKey(
        StudentGroup,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Курируемая группа'
    )

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
