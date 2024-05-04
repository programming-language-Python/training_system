from django.db import models

from apps.testing.constants import APP_NAME


class TaskType(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_default_value(class_name: str):
        if class_name == 'ClosedQuestion':
            return TaskType.objects.get_or_create(name='Закрытый вопрос')
        if class_name == 'OpenQuestion':
            return TaskType.objects.get_or_create(name='Открытый вопрос')

    class Meta:
        db_table = f'{APP_NAME}_task-type'
