from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    patronymic = models.CharField(max_length=150, blank=True, verbose_name='Отчество')
    is_teacher = models.BooleanField(default=False, verbose_name='Преподаватель')
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Группа')


class Group(models.Model):
    title = models.CharField(max_length=25, verbose_name='Группа')
