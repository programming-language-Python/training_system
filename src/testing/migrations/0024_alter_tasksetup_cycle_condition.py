# Generated by Django 4.1.4 on 2023-02-24 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0023_alter_tasksetup_operator_nesting_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksetup',
            name='cycle_condition',
            field=models.CharField(blank=True, choices=[('Простое', 'Простое'), ('Составное', 'Составное')], default=None, max_length=25, null=True, verbose_name='Условие цикла'),
        ),
    ]