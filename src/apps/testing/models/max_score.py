from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.testing.constants import APP_NAME
from apps.testing.models import Testing


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
    testing = models.ManyToManyField(
        Testing,
        related_name='max_score_set',
        verbose_name='Тестирование'
    )

    class Meta:
        db_table = f'{APP_NAME}_max-score'
