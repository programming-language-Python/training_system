from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Testing(models.Model):
    title = models.CharField(max_length=25,
                             verbose_name='Наименование')
    setting = models.ManyToManyField('TaskSetting')


class TaskSetting(models.Model):
    class IsStatement(models.TextChoices):
        is_present = True, _('Присутствует')
        absent = False, _('Отсутствует')

    class Condition(models.TextChoices):
        simple = 'Простое', _('Простое')
        composite = 'Составное', _('Составное')

    weight = models.IntegerField(verbose_name='Вес')
    is_if_statement = models.BooleanField(max_length=5,
                                          choices=IsStatement.choices,
                                          default=IsStatement.absent,
                                          verbose_name='Наличие оператора if')
    condition_of_if_statement = models.CharField(max_length=25,
                                                 choices=Condition.choices,
                                                 default=Condition.simple,
                                                 verbose_name='Условие оператора if',
                                                 blank=True)
    cycles = [
        ('while', 'while'),
        ('do-while', 'do-while'),
        ('for', 'for')
    ]
    availability_of_cycles = models.CharField(max_length=25,
                                              choices=cycles,
                                              verbose_name='Наличие одного из следующих циклов',
                                              blank=True)
    cycle_condition = models.CharField(max_length=25,
                                       choices=Condition.choices,
                                       default=Condition.simple,
                                       verbose_name='Условие оператора if',
                                       blank=True)
    operator_nesting = models.CharField(max_length=25,
                                        choices=Condition.choices,
                                        verbose_name='Условие оператора if',
                                        blank=True)


class CodeTemplate(models.Model):
    code = models.TextField(verbose_name='Код')
    setting = models.ForeignKey('TaskSetting', null=True, on_delete=models.SET_NULL)


class CompletedTesting(models.Model):
    result = models.JSONField(verbose_name='Результат теста')
    student = models.OneToOneField(settings.AUTH_USER_MODEL,
                                   on_delete=models.DO_NOTHING,
                                   verbose_name='Студент')
