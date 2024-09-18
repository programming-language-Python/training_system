from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from abstractions.abstract_models.abstract_testing import AbstractTesting
from apps.testing.constants import MAX_ASSESSMENT_THRESHOLD, MIN_ASSESSMENT_THRESHOLD, APP_NAME


class Testing(AbstractTesting):
    number = models.IntegerField(
        default=1,
        verbose_name='Номер работы'
    )
    likelihood_guessing_answers = models.FloatField(
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

    def get_absolute_url(self):
        return reverse(f'{APP_NAME}:testing_detail', kwargs={'pk': self.pk})

    def is_solving_testing_set(self) -> bool:
        return self.testing_solving_testing_set.exists()
