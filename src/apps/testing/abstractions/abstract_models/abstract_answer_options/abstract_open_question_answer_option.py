from django.db import models


class AbstractOpenQuestionAnswerOption(models.Model):
    correct_answer = models.CharField(verbose_name='Правильный ответ')

    class Meta:
        abstract = True
