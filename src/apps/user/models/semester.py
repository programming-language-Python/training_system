from django.db import models


class Semester(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True, verbose_name='Название')
    date_start = models.DateField(verbose_name='Дата начала')
    date_end = models.DateField(verbose_name='Дата окончания')

    class Meta:
        verbose_name = 'семестр'
        verbose_name_plural = 'семестры'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            start_year = self.date_start.year
            end_year = self.date_end.year % 100
            season = self._get_season()
            pre_name = f'{start_year}/{end_year} ({season})'
            self.name = self.name if self.name else pre_name
        super().save(*args, **kwargs)

    def _get_season(self):
        mid_val = self.date_end - self.date_start
        mid_val /= 2
        date = self.date_start + mid_val
        month = date.month
        if month in [1, 2, 12]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'fall'
