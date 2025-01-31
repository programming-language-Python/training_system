from django.db import models
from django.urls import reverse

from apps.user.constants import APP_NAME


class Journal(models.Model):
    absolute_journal_name = models.CharField(max_length=200, blank=True, unique=True)  # проверка наличия журнала

    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE, verbose_name='Дисциплина')
    student_group = models.ForeignKey('StudentGroup', on_delete=models.CASCADE, verbose_name='Группа')
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, verbose_name='Семестр')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, verbose_name='Преподаватель')

    class Meta:
        verbose_name = 'журнал'
        verbose_name_plural = 'журналы'

    def __str__(self) -> str:
        return (f'{self.semester.__str__()} {self.discipline.__str__()} {self.student_group.__str__()} '
                f'{self.student_group.educational_establishment.abbreviation}')

    def save(self, *args, **kwargs):
        if not self.id:
            semester = self.semester.__str__()
            discipline = self.discipline.__str__()
            student_group = self.student_group.__str__()
            teacher = self.teacher.id
            educational_establishment = self.student_group.educational_establishment.abbreviation
            self.absolute_journal_name = (f'{semester}_{discipline}_{student_group}_{educational_establishment}_'
                                          f'{teacher}')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(f'{APP_NAME}:testing_list', kwargs={'journal_pk': self.pk})
