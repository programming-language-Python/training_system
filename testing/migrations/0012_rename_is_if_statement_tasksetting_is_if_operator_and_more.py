# Generated by Django 4.1.4 on 2023-01-07 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0011_alter_tasksetting_user_alter_testing_setting_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasksetting',
            old_name='is_if_statement',
            new_name='is_if_operator',
        ),
        migrations.AlterField(
            model_name='tasksetting',
            name='title',
            field=models.CharField(max_length=25, verbose_name='Наименование'),
        ),
    ]
