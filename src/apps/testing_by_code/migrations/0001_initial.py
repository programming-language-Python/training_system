# Generated by Django 4.2.4 on 2024-05-02 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Цикл')),
            ],
            options={
                'verbose_name': 'Цикл',
                'verbose_name_plural': 'Циклы',
            },
        ),
        migrations.CreateModel(
            name='OperatorNesting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Вложенность операторов')),
            ],
            options={
                'verbose_name': 'Вложенность оператора',
                'verbose_name_plural': 'Вложенность операторов',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_if_operator', models.CharField(choices=[('Присутствует', 'Присутствует'), ('Отсутствует', 'Отсутствует')], default='Отсутствует', max_length=50, verbose_name='Наличие оператора if')),
                ('condition_of_if_operator', models.CharField(blank=True, choices=[('Простое', 'Простое'), ('Составное', 'Составное')], max_length=50, null=True, verbose_name='Условие оператора if')),
                ('cycle_condition', models.CharField(blank=True, choices=[('Простое', 'Простое'), ('Составное', 'Составное')], max_length=50, null=True, verbose_name='Условие цикла')),
                ('is_OOP', models.BooleanField(default=False, verbose_name='ООП')),
                ('is_strings', models.BooleanField(default=False, verbose_name='Строки')),
                ('cycle', models.ManyToManyField(blank=True, to='testing_by_code.cycle', verbose_name='Цикл')),
                ('operator_nesting', models.ManyToManyField(blank=True, to='testing_by_code.operatornesting', verbose_name='Вложенность операторов')),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Пользователи')),
            ],
            options={
                'verbose_name': 'Настройка',
                'verbose_name_plural': 'Настройки',
            },
        ),
        migrations.CreateModel(
            name='Testing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Наименование')),
                ('is_published', models.BooleanField(blank=True, default=False, verbose_name='Опубликовано')),
                ('is_review_of_result_by_student', models.BooleanField(blank=True, default=True, verbose_name='Просмотр результата студентом')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_of_deletion', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата удаления')),
                ('task_lead_time', models.TimeField(blank=True, default=None, null=True, verbose_name='Время выполнения задачи')),
                ('total_weight', models.IntegerField()),
                ('student_groups', models.ManyToManyField(blank=True, related_name='%(app_label)s_%(class)s_set', to='user.studentgroup', verbose_name='Группы студентов')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Тестирование',
                'verbose_name_plural': 'Тестирования',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=1, verbose_name='Вес')),
                ('count', models.IntegerField(default=0, verbose_name='Количество')),
                ('setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing_by_code.setting', verbose_name='Настройка')),
                ('testing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing_by_code.testing', verbose_name='Тестирование')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='SolvingTesting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Наименование')),
                ('assessment', models.IntegerField(null=True, verbose_name='Оценка')),
                ('start_passage', models.DateTimeField(auto_now_add=True, verbose_name='Начало прохождения')),
                ('end_passage', models.DateTimeField(default=None, null=True, verbose_name='Окончание прохождения')),
                ('total_weight', models.IntegerField(verbose_name='Общий вес')),
                ('weight_of_student_tasks', models.IntegerField(verbose_name='Вес задач студента')),
                ('tasks', models.JSONField(verbose_name='Задачи')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_solving_testing_set', to='user.student', verbose_name='Студент')),
                ('testing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_solving_testing_set', to='testing_by_code.testing', verbose_name='Тестирование')),
            ],
            options={
                'verbose_name': 'Решение тестирования',
                'verbose_name_plural': 'Решения тестирований',
                'abstract': False,
            },
        ),
    ]
