# Generated by Django 4.1.4 on 2023-01-18 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testing', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testing',
            name='student_group',
            field=models.ManyToManyField(to='user.studentgroup', verbose_name='Группы студентов'),
        ),
        migrations.AddField(
            model_name='testing',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='tasksetting',
            name='presence_one_of_following_cycles',
            field=models.ManyToManyField(blank=True, to='testing.cycle', verbose_name='Наличие одного из следующих циклов'),
        ),
        migrations.AddField(
            model_name='tasksetting',
            name='operator_nesting',
            field=models.ManyToManyField(blank=True, to='testing.operatornesting', verbose_name='Вложенность операторов'),
        ),
        migrations.AddField(
            model_name='tasksetting',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='completedtesting',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Студент'),
        ),
        migrations.AddField(
            model_name='codetemplate',
            name='setting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.tasksetting', verbose_name='Настройки'),
        ),
    ]