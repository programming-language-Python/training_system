# Generated by Django 4.2.4 on 2024-02-25 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0031_closedquestionansweroptionstudent_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='openquestionansweroptioncorrect',
            table='testing_openQuestion_answerOption_correct',
        ),
    ]