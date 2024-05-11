from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse

from apps.user.constants import APP_NAME


class User(AbstractUser):
    patronymic = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Отчество'
    )

    def get_absolute_url(self):
        return reverse(APP_NAME + ':testing_completed_list', kwargs={"pk": self.pk})

    def is_teacher(self) -> bool:
        try:
            return bool(self.teacher)
        except ObjectDoesNotExist:
            return False

    def get_full_name(self):
        """
        Return the last_name plus the first_name (plus the patronymic), with a space in between.
        """
        full_name = '%s %s %s' % (self.last_name, self.first_name, self.patronymic)
        return full_name.strip()

    def get_full_name_initials(self):
        """
        Return the last_name plus the first_name (plus the patronymic), with a space in between. (first_name and patronymic is initials)
        """
        initials = ''
        initials += self.first_name[0] + '.' if self.first_name else ''
        initials += self.patronymic[0] + '.' if self.patronymic else ''
        full_name_initials = '%s %s' % (self.last_name, initials)
        return full_name_initials.strip()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
