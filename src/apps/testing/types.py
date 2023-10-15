from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskOrder(models.TextChoices):
    SIMPLE = 'Случайный', _('Случайный')
    COMPOSITE = 'Установленный', _('Установленный')
