from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from abstractions.abstract_models.abstract_testing import AbstractTesting
from apps.testing.constants import MAX_ASSESSMENT_THRESHOLD, MIN_ASSESSMENT_THRESHOLD, APP_NAME


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
            MaxValueValidator(MAX_ASSESSMENT_THRESHOLD),
            MinValueValidator(MIN_ASSESSMENT_THRESHOLD)
        ],
        verbose_name='Пороговое значение оценки'
    )
    is_established_order_tasks = models.BooleanField(
        verbose_name='Установленный порядок задач',
        default=False
    )
    task_lead_time = models.TimeField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Время выполнения задачи'
    )

    def get_absolute_url(self):
        return reverse(APP_NAME + ':testing_detail', kwargs={'pk': self.pk})


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
