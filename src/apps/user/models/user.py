from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class User(AbstractUser):
    patronymic = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Отчество'
    )

    def is_teacher(self) -> bool:
        try:
            return bool(self.teacher)
        except ObjectDoesNotExist:
            return False

    def get_full_name(self):
        full_name = '%s %s %s' % (self.last_name, self.first_name, self.patronymic)
        return full_name.strip()

    def get_full_name_initials(self):
        initials = ''
        initials += self.first_name[0] + '.' if self.first_name else ''
        initials += self.patronymic[0] + '.' if self.patronymic else ''
        full_name_initials = '%s %s' % (self.last_name, initials)
        return full_name_initials.strip()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
