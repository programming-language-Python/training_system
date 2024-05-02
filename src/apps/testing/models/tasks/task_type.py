from django.db import models

from apps.testing.constants import APP_NAME


class TaskType(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')

    class Meta:
        db_table = f'{APP_NAME}_task-type'
