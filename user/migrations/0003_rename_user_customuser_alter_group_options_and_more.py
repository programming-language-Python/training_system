# Generated by Django 4.1.4 on 2023-01-01 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('testing', '0005_alter_tasksetting_condition_of_if_statement_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('user', '0002_alter_group_options_alter_user_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='CustomUser',
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Группа студента', 'verbose_name_plural': 'Группы студентов'},
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=25, verbose_name='Группа студента'),
        ),
    ]
