# Generated by Django 4.1.4 on 2023-01-31 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testing', '0014_codetemplate_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedtesting',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Студент'),
        ),
    ]