from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from testing.utils.utils import round_up
from user.models import User, StudentGroup

app_name = 'testing'


class Task(models.Model):
    weight = models.IntegerField(default=1, verbose_name='Вес')
    testing = models.ForeignKey('Testing',
                                on_delete=models.CASCADE,
                                verbose_name='Тестирование')
    task_setup = models.ForeignKey('TaskSetup',
                                   on_delete=models.CASCADE,
                                   verbose_name='Настройка задачи')
    count = models.IntegerField(default=0,
                                verbose_name='Количество')

    def get_absolut_url(self):
        return reverse(app_name + ':task_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Testing(models.Model):
    title = models.CharField(max_length=25,
                             verbose_name='Наименование',
                             unique=True)
    student_groups = models.ManyToManyField(StudentGroup,
                                            verbose_name='Группы студентов')
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             verbose_name='Пользователь')
    is_published = models.BooleanField(blank=True,
                                       default=True,
                                       verbose_name='Опубликовано')

    def get_absolute_url(self):
        return reverse(app_name + ':testing_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тестирование'
        verbose_name_plural = 'Тестирования'


class TaskSetup(models.Model):
    class IsOperator(models.TextChoices):
        be_present = 'Присутствует', _('Присутствует')
        absent = 'Отсутствует', _('Отсутствует')

    class Condition(models.TextChoices):
        simple = 'Простое', _('Простое')
        composite = 'Составное', _('Составное')

    # use_of_all_variables = models.BooleanField(default=False,
    #                                            verbose_name='Использование обязательно всех переменных')
    # TODO Сделать тип bool
    is_if_operator = models.CharField(max_length=25,
                                      choices=IsOperator.choices,
                                      default=IsOperator.absent,
                                      verbose_name='Наличие оператора if')
    condition_of_if_operator = models.CharField(max_length=25,
                                                choices=Condition.choices,
                                                blank=True,
                                                null=True,
                                                verbose_name='Условие оператора if')
    presence_one_of_cycles = models.ManyToManyField('Cycle',
                                                    blank=True,
                                                    # null=True,
                                                    verbose_name='Наличие одного из следующих циклов')
    cycle_condition = models.CharField(max_length=25,
                                       choices=Condition.choices,
                                       blank=True,
                                       null=True,
                                       verbose_name='Условие цикла')
    operator_nesting = models.ManyToManyField('OperatorNesting',
                                              blank=True,
                                              # null=True,
                                              verbose_name='Вложенность операторов')
    is_OOP = models.BooleanField(default=False,
                                 verbose_name='ООП')
    is_strings = models.BooleanField(default=False,
                                     verbose_name='Строки')
    users = models.ManyToManyField(User,
                                   blank=True,
                                   verbose_name='Пользователи')

    def get_absolute_url(self):
        return reverse(app_name + ':task_setup_detail',
                       kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Настройка задачи'
        verbose_name_plural = 'Настройки задач'


class Cycle(models.Model):
    title = models.CharField(max_length=25,
                             verbose_name='Цикл')

    def get_absolute_url(self):
        return reverse('cycle_detail',
                       kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Цикл'
        verbose_name_plural = 'Циклы'


class OperatorNesting(models.Model):
    title = models.CharField(max_length=25,
                             verbose_name='Вложенность операторов')

    def get_absolute_url(self):
        return reverse('operator_nesting_detail',
                       kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вложенность оператора'
        verbose_name_plural = 'Вложенность операторов'


class CompletedTesting(models.Model):
    assessment = models.IntegerField(verbose_name='Оценка')
    total_weight = models.IntegerField(verbose_name='Общий вес')
    weight_of_student_tasks = models.IntegerField(
        verbose_name='Вес задач студента')
    tasks = models.JSONField(verbose_name='Задачи')
    testing = models.ForeignKey(Testing,
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name='Тестирование')
    # date_of_passage = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='Студент')

    def get_absolute_url(self):
        return reverse('complete_testing_detail',
                       kwargs={'pk': self.pk})

    def get_assessment_in_percentage(self):
        return round_up(self.weight_of_student_tasks / self.total_weight * 100)

    class Meta:
        verbose_name = 'Завершённое тестирование'
        verbose_name_plural = 'Завершённые тестирования'
