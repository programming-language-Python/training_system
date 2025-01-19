from django.db import models


class Discipline(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    semesters = models.ManyToManyField(
        'Semester',
        related_name='disciplines',
        through='Schedule',
        verbose_name='Семестр'
    )
    student_groups = models.ManyToManyField(
        'StudentGroup',
        related_name='disciplines',
        through='Schedule',
        verbose_name='Группа'
    )

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
        return self.name
