# Generated by Django 4.2.4 on 2024-06-17 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing_by_code', '0003_alter_testing_total_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='count',
            field=models.IntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='task',
            name='setting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_set', to='testing_by_code.setting', verbose_name='Настройка'),
        ),
        migrations.AlterField(
            model_name='task',
            name='testing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_set', to='testing_by_code.testing', verbose_name='Тестирование'),
        ),
    ]
