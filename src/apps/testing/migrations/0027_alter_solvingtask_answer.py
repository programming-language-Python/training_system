# Generated by Django 4.2.4 on 2025-03-11 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0026_alter_solvingtask_options_alter_solvingtask_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solvingtask',
            name='answer',
            field=models.JSONField(blank=True, null=True, verbose_name='Ответ'),
        ),
    ]
