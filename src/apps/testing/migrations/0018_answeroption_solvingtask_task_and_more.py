# Generated by Django 4.2.4 on 2024-12-22 18:33

from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0017_alter_sequencingansweroption_sequencing'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField(blank=True, verbose_name='Порядковый номер')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Правильный')),
            ],
            options={
                'ordering': ['serial_number'],
            },
        ),
        migrations.CreateModel(
            name='SolvingTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=100, verbose_name='Ответ')),
                ('start_passage', models.DateTimeField(blank=True, null=True, verbose_name='Начало прохождения')),
                ('lead_time', models.TimeField(blank=True, null=True, verbose_name='Время выполнения')),
                ('solving_testing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solving_task_set', to='testing.solvingtesting', verbose_name='Решение тестирования')),
            ],
            options={
                'db_table': 'testing_solving-task',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField(blank=True, verbose_name='Порядковый номер')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание')),
                ('lead_time', models.TimeField(blank=True, default=None, null=True, verbose_name='Время выполнения')),
                ('type', models.CharField(choices=[('Закрытый вопрос', 'Закрытый вопрос'), ('Открытый вопрос', 'Открытый вопрос'), ('Установление последовательности', 'Установление последовательности')], max_length=50, verbose_name='Тип')),
            ],
            options={
                'ordering': ['serial_number'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='openquestion',
            name='task_type',
        ),
        migrations.RemoveField(
            model_name='openquestion',
            name='testing',
        ),
        migrations.RemoveField(
            model_name='sequencing',
            name='task_type',
        ),
        migrations.RemoveField(
            model_name='sequencing',
            name='testing',
        ),
        migrations.RemoveField(
            model_name='sequencingansweroption',
            name='sequencing',
        ),
        migrations.RemoveField(
            model_name='solvingclosedquestion',
            name='solving_testing',
        ),
        migrations.RemoveField(
            model_name='solvingclosedquestion',
            name='task',
        ),
        migrations.RemoveField(
            model_name='solvingopenquestion',
            name='solving_testing',
        ),
        migrations.RemoveField(
            model_name='solvingopenquestion',
            name='task',
        ),
        migrations.RemoveField(
            model_name='solvingsequencing',
            name='solving_testing',
        ),
        migrations.RemoveField(
            model_name='solvingsequencing',
            name='task',
        ),
        migrations.AlterModelOptions(
            name='closedquestion',
            options={},
        ),
        migrations.RemoveField(
            model_name='closedquestion',
            name='description',
        ),
        migrations.RemoveField(
            model_name='closedquestion',
            name='lead_time',
        ),
        migrations.RemoveField(
            model_name='closedquestion',
            name='serial_number',
        ),
        migrations.RemoveField(
            model_name='closedquestion',
            name='task_type',
        ),
        migrations.RemoveField(
            model_name='closedquestion',
            name='testing',
        ),
        migrations.RemoveField(
            model_name='maxscore',
            name='testing',
        ),
        migrations.RemoveField(
            model_name='openquestionansweroption',
            name='open_question',
        ),
        migrations.RemoveField(
            model_name='testing',
            name='likelihood_guessing_answers',
        ),
        migrations.AddField(
            model_name='testing',
            name='max_score',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='testing.maxscore', verbose_name='Максимальный балл'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testing',
            name='probability_of_guessing',
            field=models.FloatField(default=1, verbose_name='Вероятность угадывания'),
        ),
        migrations.AlterField(
            model_name='closedquestion',
            name='is_partially_correct_execution',
            field=models.BooleanField(default=False, verbose_name='Учет частично верного выполнения'),
        ),
        migrations.AlterField(
            model_name='closedquestion',
            name='is_several_correct_answers',
            field=models.BooleanField(default=False, verbose_name='Несколько правильных ответов'),
        ),
        migrations.DeleteModel(
            name='ClosedQuestionAnswerOption',
        ),
        migrations.DeleteModel(
            name='OpenQuestion',
        ),
        migrations.DeleteModel(
            name='Sequencing',
        ),
        migrations.DeleteModel(
            name='SequencingAnswerOption',
        ),
        migrations.DeleteModel(
            name='SolvingClosedQuestion',
        ),
        migrations.DeleteModel(
            name='SolvingOpenQuestion',
        ),
        migrations.DeleteModel(
            name='SolvingSequencing',
        ),
        migrations.DeleteModel(
            name='TaskType',
        ),
        migrations.AddField(
            model_name='solvingtask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solving_task_set', to='testing.task', verbose_name='Задача'),
        ),
    ]
