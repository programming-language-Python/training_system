# Generated by Django 4.2.4 on 2024-01-02 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0005_alter_completedtesting_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testing',
            name='lead_time',
        ),
    ]