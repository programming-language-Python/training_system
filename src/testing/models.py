from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from testing.utils.utils import round_up
from user.models import User, StudentGroup

app_name = 'testing'
MAX_LENGTH = 50


class Task(models.Model):
    weight = models.IntegerField(default=1, verbose_name='Вес')
    testing = models.ForeignKey(
        'Testing',
        on_delete=models.CASCADE,
        verbose_name='Тестирование'
    )
    setting = models.ForeignKey(
        'Setting',
        on_delete=models.CASCADE,
        verbose_name='Настройка'
    )
    count = models.IntegerField(
        default=0,
        verbose_name='Количество'
    )

    def get_absolut_url(self):
        return reverse(app_name + ':task_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Testing(models.Model):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Наименование',
        unique=True
    )
    student_groups = models.ManyToManyField(
        StudentGroup,
        verbose_name='Группы студентов'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Пользователь'
    )
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

    def get_absolute_url(self):
        return reverse(app_name + ':testing_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тестирование'
        verbose_name_plural = 'Тестирования'


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
        return reverse(app_name + ':setting_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class Cycle(models.Model):
    title = models.CharField(max_length=MAX_LENGTH, verbose_name='Цикл')

    def get_absolute_url(self):
        return reverse('cycle_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Цикл'
        verbose_name_plural = 'Циклы'


class OperatorNesting(models.Model):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Вложенность операторов'
    )

    def get_absolute_url(self):
        return reverse('operator_nesting_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вложенность оператора'
        verbose_name_plural = 'Вложенность операторов'


class CompletedTesting(models.Model):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Наименование',
        unique=True
    )
    assessment = models.IntegerField(verbose_name='Оценка')
    total_weight = models.IntegerField(verbose_name='Общий вес')
    weight_of_student_tasks = models.IntegerField(verbose_name='Вес задач студента')
    tasks = models.JSONField(verbose_name='Задачи')
    testing = models.ForeignKey(
        Testing,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тестирование'
    )
    start_passage = models.DateTimeField(verbose_name='Начало прохождения')
    end_passage = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Окончание прохождения'
    )
    is_review_of_result_by_student = models.BooleanField(
        blank=True,
        default=True,
        verbose_name='Просмотр результата студентом'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Студент'
    )

    def get_absolute_url(self):
        return reverse('complete_testing_detail', kwargs={'pk': self.pk})

    def get_assessment_in_percentage(self):
        return round_up(self.weight_of_student_tasks / self.total_weight * 100)

    class Meta:
        verbose_name = 'Завершённое тестирование'
        verbose_name_plural = 'Завершённые тестирования'
