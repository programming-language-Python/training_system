# Generated by Django 4.2.4 on 2024-08-23 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0009_rename_closed_question_solvingclosedquestion_task_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solvingtesting',
            name='duration',
            field=models.DurationField(null=True, verbose_name='Длительность теста'),
        ),
    ]
