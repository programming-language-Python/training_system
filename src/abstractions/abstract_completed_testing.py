from django.db import models

from abstractions.abstract_fields import AbstractFieldTitle
from apps.testing_by_code.utils.utils import round_up
from config import settings


class AbstractCompletedTesting(AbstractFieldTitle):
    assessment = models.IntegerField(verbose_name='Оценка')
    total_weight = models.IntegerField(verbose_name='Общий вес')
    weight_of_student_tasks = models.IntegerField(verbose_name='Вес задач студента')
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
        related_name='%(app_label)s_%(class)s_related',
        verbose_name='Студент'
    )

    def get_assessment_in_percentage(self):
        return round_up(self.weight_of_student_tasks / self.total_weight * 100)

    class Meta:
        abstract = True
        verbose_name = 'Завершённое тестирование'
        verbose_name_plural = 'Завершённые тестирования'
