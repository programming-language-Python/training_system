# Generated by Django 4.1.4 on 2023-03-18 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('м', 'Мужской'), ('ж', 'Женский')], default='м', max_length=1, verbose_name='Пол'),
        ),
    ]
