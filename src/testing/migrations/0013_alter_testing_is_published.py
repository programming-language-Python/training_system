# Generated by Django 4.1.4 on 2023-01-24 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0012_alter_task_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testing',
            name='is_published',
            field=models.BooleanField(blank=True, default=True, verbose_name='Опубликовано'),
        ),
    ]