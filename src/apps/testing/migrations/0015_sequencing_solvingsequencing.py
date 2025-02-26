# Generated by Django 4.2.4 on 2024-09-18 19:18

from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0014_alter_maxscore_five_alter_maxscore_four_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sequencing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField(blank=True, verbose_name='Порядковый номер')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание')),
                ('lead_time', models.TimeField(blank=True, default=None, null=True, verbose_name='Время выполнения')),
                ('is_correct', models.BooleanField(verbose_name='Правильный')),
                ('task_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sequencing_set', to='testing.tasktype', verbose_name='Тип задачи')),
                ('testing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sequencing_set', to='testing.testing', verbose_name='Тестирование')),
            ],
            options={
                'ordering': ['serial_number'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SolvingSequencing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=100, verbose_name='Ответ')),
                ('start_passage', models.DateTimeField(blank=True, null=True, verbose_name='Начало прохождения')),
                ('lead_time', models.TimeField(blank=True, null=True, verbose_name='Время выполнения')),
                ('solving_testing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solving_sequencing_set', to='testing.solvingtesting', verbose_name='Решение тестирования')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solving_sequencing_set', to='testing.sequencing', verbose_name='Установление последовательности')),
            ],
            options={
                'db_table': 'testing_solving-sequencing',
            },
        ),
    ]
