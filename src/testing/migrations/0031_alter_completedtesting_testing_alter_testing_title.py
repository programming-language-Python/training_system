# Generated by Django 4.1.4 on 2023-03-18 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0030_remove_tasksetup_use_of_all_variables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedtesting',
            name='testing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='testing.testing', verbose_name='Тестирование'),
        ),
        migrations.AlterField(
            model_name='testing',
            name='title',
            field=models.CharField(max_length=25, unique=True, verbose_name='Наименование'),
        ),
    ]