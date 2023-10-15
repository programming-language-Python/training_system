from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from abstractions import AbstractTesting
from apps.testing.types import TaskOrder


class Testing(AbstractTesting):
    number = models.IntegerField(verbose_name='Номер работы')
    likelihood_guessing_answers = models.FloatField(
        max_length=1,
        default=1,
        verbose_name='Вероятность угадывания правильных ответов'
    )
    assessment_threshold = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        verbose_name='Пороговое значение оценки'
    )
    task_order = models.CharField(
        choices=TaskOrder.choices,
        verbose_name='Порядок задач'
    )
    lead_time = models.TimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Время выполнения'
    )
    task_lead_time = models.TimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Время выполнения задачи'
    )


class MaxScore(models.Model):
    five = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        verbose_name='Отлично'
    )
    four = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        verbose_name='Хорошо'
    )
    three = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        verbose_name='Удовлетворительно'
    )
    two = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        verbose_name='Неудовлетворительно'
    )
    testing = models.OneToOneField(
        Testing,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Тестирование'
    )

    class Meta:
        db_table = 'testing_testing_maxScore'
