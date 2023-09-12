from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

MAX_LENGTH = 50


class User(AbstractUser):
    patronymic = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Отчество'
    )
    is_teacher = models.BooleanField(
        default=False,
        verbose_name='Преподаватель'
    )
    student_group = models.ForeignKey(
        'StudentGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Группа студента'
    )

    def get_absolute_url(self):
        return reverse('user:testing_completed_list', kwargs={"pk": self.pk})
        # if self.is_teacher:
        #     return reverse('testing_completed_list', kwargs={"pk": self.pk})
        # return reverse('user_detail', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class StudentGroup(models.Model):
    title = models.CharField(max_length=25, verbose_name='Группа студента')

    def get_absolute_url(self):
        return reverse('student_group_detail', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа студента'
        verbose_name_plural = 'Группы студентов'


class UnfinishedTesting(models.Model):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Наименование',
        unique=True
    )
    tasks = models.JSONField(verbose_name='Задачи')
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Студент'
    )

    class Meta:
        verbose_name = 'Незавершённое тестирование'
        verbose_name_plural = 'Незавершённые тестирования'
