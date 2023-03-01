from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    patronymic = models.CharField(max_length=150, blank=True, verbose_name='Отчество')
    is_teacher = models.BooleanField(default=False, verbose_name='Преподаватель')
    student_group = models.ForeignKey('StudentGroup', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name='Группа студента')

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
