# Generated by Django 4.2.4 on 2025-01-26 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_discipline_semester_schedule_discipline_semesters_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='user',
            new_name='teacher',
        ),
    ]
