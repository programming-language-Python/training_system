from django.db import models
from django.urls import reverse

from apps.user.constants import APP_NAME
from apps.user.models import StudentGroup
from config.settings import AUTH_USER_MODEL


class Student(models.Model):
    version_in_group = models.IntegerField(blank=True, verbose_name='Номер варианта в группе')
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    student_group = models.ForeignKey(
        StudentGroup,
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )

    def get_absolute_url(self) -> reverse:
        return reverse(f'{APP_NAME}:student_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.id:
            self.version_in_group = self.version_in_group if self.version_in_group else 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.get_full_name()

    def __unicode__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
