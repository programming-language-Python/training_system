# Generated by Django 4.2.4 on 2024-03-17 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0033_alter_completedtesting_assessment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedtesting',
            name='end_passage',
            field=models.DateTimeField(null=True, verbose_name='Окончание прохождения'),
        ),
        migrations.AlterField(
            model_name='completedtesting',
            name='start_passage',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Начало прохождения'),
        ),
        migrations.AlterField(
            model_name='completedtesting',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='Наименование'),
        ),
    ]