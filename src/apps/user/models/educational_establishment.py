from django.db import models

from apps.user.constants import APP_NAME


class EducationalEstablishment(models.Model):
    full_name = models.CharField(max_length=50, unique=True, verbose_name='Полное название')
    abbreviation = models.CharField(max_length=50, unique=True, verbose_name='Аббревиатура')

    def __str__(self):
        return f'{self.abbreviation}({self.full_name})'

    class Meta:
        verbose_name = 'Образовательное учреждение'
        verbose_name_plural = 'Образовательные учреждения'
        db_table = f'{APP_NAME}_educational-establishment'
