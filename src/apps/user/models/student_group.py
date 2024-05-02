from django.db import models
from django.urls import reverse

from apps.user.constants import APP_NAME
from apps.user.models import EducationalEstablishment


class StudentGroup(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    year_start_studying = models.IntegerField(verbose_name='Год начала обучения')
    year_end_studying = models.IntegerField(verbose_name='Год окончания обучения')
    specialty = models.CharField(max_length=50, blank=True, verbose_name='Специальность')
    educational_establishment = models.ForeignKey(
        EducationalEstablishment,
        on_delete=models.CASCADE,
        related_name='student_group_set',
        verbose_name='Образовательное учреждение'
    )

    def get_absolute_url(self):
        return reverse('student_group_detail', kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа студента'
        verbose_name_plural = 'Группы студентов'
        db_table = f'{APP_NAME}_student-group'
