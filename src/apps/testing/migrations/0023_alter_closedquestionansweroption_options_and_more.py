# Generated by Django 4.2.4 on 2024-02-07 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0022_openquestionansweroption'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='closedquestionansweroption',
            options={},
        ),
        migrations.AlterModelOptions(
            name='openquestion',
            options={'ordering': ['serial_number']},
        ),
        migrations.RemoveField(
            model_name='openquestion',
            name='correct_answer',
        ),
        migrations.AlterField(
            model_name='openquestionansweroption',
            name='open_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='open_question_answer_option_set', to='testing.openquestion', verbose_name='Открытый вопрос'),
        ),
    ]