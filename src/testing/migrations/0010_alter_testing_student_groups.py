# Generated by Django 4.2.4 on 2023-08-11 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_user_gender'),
        ('testing', '0009_completedtesting_testing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testing',
            name='student_groups',
            field=models.ManyToManyField(blank=True, to='user.studentgroup', verbose_name='Группы студентов'),
        ),
    ]