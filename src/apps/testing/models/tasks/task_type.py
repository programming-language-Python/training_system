from django.db import models

from apps.testing.constants import APP_NAME
from apps.testing.types import TaskData


class TaskType(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')

    def __str__(self) -> str:
        return self.name

    def get_data(self):
        task_data = {
            'Закрытый вопрос': TaskData(name='closed_question'),
            'Открытый вопрос': TaskData(name='open_question'),
            'Установление последовательности': TaskData(name='sequencing')
        }
        return task_data[self.name]

    class Meta:
        db_table = f'{APP_NAME}_task-type'
