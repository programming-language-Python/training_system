# Generated by Django 4.1.4 on 2023-01-25 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0013_alter_testing_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='codetemplate',
            name='answer',
            field=models.CharField(default=1, max_length=20, verbose_name='Ответ'),
            preserve_default=False,
        ),
    ]