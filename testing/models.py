from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from user.models import User, StudentGroup

app_name = 'testing'


class Testing(models.Model):
    title = models.CharField(max_length=25,
                             verbose_name='Наименование')
    setting = models.ForeignKey('TaskSetting', on_delete=models.CASCADE, verbose_name='Настройки')
    student_group = models.ManyToManyField(StudentGroup, verbose_name='Группы студентов')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')

    def get_absolute_url(self):
        return reverse(app_name + ':testing_update', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Тестирование'
        verbose_name_plural = 'Тестирования'


class TaskSetting(models.Model):
    class IsOperator(models.TextChoices):
        be_present = 'Присутствует', _('Присутствует')
        absent = 'Отсутствует', _('Отсутствует')

    class Condition(models.TextChoices):
        simple = 'Простое', _('Простое')
        composite = 'Составное', _('Составное')

    weight = models.IntegerField(verbose_name='Вес')
    is_if_operator = models.CharField(max_length=25,
                                      choices=IsOperator.choices,
                                      default=IsOperator.absent,
                                      verbose_name='Наличие оператора if')
    condition_of_if_operator = models.CharField(max_length=25,
                                                choices=Condition.choices,
                                                blank=True,
                                                null=True,
                                                default=None,
                                                verbose_name='Условие оператора if')
    availability_of_cycles = models.ManyToManyField('Cycle', blank=True, verbose_name='Наличие цикла')
    cycle_condition = models.CharField(max_length=25,
                                       choices=Condition.choices,
                                       blank=True,
                                       null=True,
                                       default=None,
                                       verbose_name='Условие цикла')
    operator_nesting = models.ManyToManyField('OperatorNesting', blank=True, verbose_name='Вложенность операторов')
    user = models.ManyToManyField(User, verbose_name='Пользователи')

    def get_absolute_url(self):
        return reverse('tasksetting_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Настройка задачи'
        verbose_name_plural = 'Настройки задач'


class Cycle(models.Model):
    title = models.CharField(max_length=25, verbose_name='Цикл')

    def get_absolute_url(self):
        return reverse('cycle_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Цикл'
        verbose_name_plural = 'Циклы'


class OperatorNesting(models.Model):
    title = models.CharField(max_length=25, verbose_name='Вложенность операторов')

    def get_absolute_url(self):
        return reverse('operator_nesting_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вложенность оператора'
        verbose_name_plural = 'Вложенность операторов'


class CodeTemplate(models.Model):
    code = models.TextField(verbose_name='Код')
    setting = models.ForeignKey('TaskSetting', null=True, on_delete=models.SET_NULL, verbose_name='Настройка')

    def get_absolute_url(self):
        return reverse('code_template_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Шаблон кода'
        verbose_name_plural = 'Шаблоны кодов'


class CompletedTesting(models.Model):
    result = models.JSONField(verbose_name='Результат теста')
    student = models.OneToOneField(settings.AUTH_USER_MODEL,
                                   on_delete=models.DO_NOTHING,
                                   verbose_name='Студент')

    def get_absolute_url(self):
        return reverse('complete_testing_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Завершённое тестирование'
        verbose_name_plural = 'Завершённые тестирования'
