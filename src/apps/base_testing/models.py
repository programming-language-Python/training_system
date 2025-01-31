from typing import Iterable

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class MaxScore(models.Model):
    five = models.IntegerField(
        default=100,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        verbose_name='Отлично'
    )
    four = models.IntegerField(
        default=80,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        verbose_name='Хорошо'
    )
    three = models.IntegerField(
        default=60,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        verbose_name='Удовлетворительно'
    )
    two = models.IntegerField(
        default=40,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        verbose_name='Неудовлетворительно'
    )

    def get_fields(self) -> Iterable:
        from services import get_model_fields
        return get_model_fields(
            model=self,
            excluded_fields=['id']
        )

    class Meta:
        db_table = f'base-testing_max-score'
