# Generated by Django 4.2.4 on 2024-02-05 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0020_openquestion_serial_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='closedquestion',
            name='weight',
        ),
        migrations.RemoveField(
            model_name='openquestion',
            name='weight',
        ),
        migrations.AlterField(
            model_name='closedquestionansweroption',
            name='serial_number',
            field=models.IntegerField(blank=True, verbose_name='Порядковый номер'),
        ),
    ]