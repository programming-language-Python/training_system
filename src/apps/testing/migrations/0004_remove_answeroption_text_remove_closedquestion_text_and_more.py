# Generated by Django 4.2.4 on 2023-12-28 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testing', '0003_closedquestion_testing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answeroption',
            name='text',
        ),
        migrations.RemoveField(
            model_name='closedquestion',
            name='text',
        ),
        migrations.RemoveField(
            model_name='testing',
            name='task_order',
        ),
        migrations.AddField(
            model_name='answeroption',
            name='description',
            field=models.TextField(default=1, verbose_name='Описание'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='closedquestion',
            name='description',
            field=models.TextField(default=1, verbose_name='Описание'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testing',
            name='is_established_order_tasks',
            field=models.BooleanField(default=False, verbose_name='Установленный порядок задач'),
        ),
        migrations.CreateModel(
            name='CompletedTesting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Наименование')),
                ('assessment', models.IntegerField(verbose_name='Оценка')),
                ('total_weight', models.IntegerField(verbose_name='Общий вес')),
                ('weight_of_student_tasks', models.IntegerField(verbose_name='Вес задач студента')),
                ('start_passage', models.DateTimeField(verbose_name='Начало прохождения')),
                ('end_passage', models.DateTimeField(auto_now_add=True, verbose_name='Окончание прохождения')),
                ('is_review_of_result_by_student', models.BooleanField(blank=True, default=True, verbose_name='Просмотр результата студентом')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'db_table': 'testing_complitedTesting',
            },
        ),
    ]