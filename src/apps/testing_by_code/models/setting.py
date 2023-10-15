from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.testing_by_code.constants import APP_NAME
from apps.user.models import User
from config.settings import MAX_LENGTH


class Setting(models.Model):
    class OperatorPresenceType(models.TextChoices):
        BE_PRESENT = 'Присутствует', _('Присутствует')
        ABSENT = 'Отсутствует', _('Отсутствует')

    class ConditionType(models.TextChoices):
        SIMPLE = 'Простое', _('Простое')
        COMPOSITE = 'Составное', _('Составное')

    # TODO Сделать тип bool
    is_if_operator = models.CharField(
        max_length=MAX_LENGTH,
        choices=OperatorPresenceType.choices,
        default=OperatorPresenceType.ABSENT,
        verbose_name='Наличие оператора if'
    )
    condition_of_if_operator = models.CharField(
        max_length=MAX_LENGTH,
        choices=ConditionType.choices,
        blank=True,
        null=True,
        verbose_name='Условие оператора if'
    )
    cycle = models.ManyToManyField(
        'Cycle',
        blank=True,
        # null=True,
        verbose_name='Цикл'
    )
    cycle_condition = models.CharField(
        max_length=MAX_LENGTH,
        choices=ConditionType.choices,
        blank=True,
        null=True,
        verbose_name='Условие цикла'
    )
    operator_nesting = models.ManyToManyField(
        'OperatorNesting',
        blank=True,
        # null=True,
        verbose_name='Вложенность операторов'
    )
    is_OOP = models.BooleanField(default=False, verbose_name='ООП')
    is_strings = models.BooleanField(default=False, verbose_name='Строки')
    users = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='Пользователи'
    )

    def get_absolute_url(self):
        return reverse(APP_NAME + ':setting_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
