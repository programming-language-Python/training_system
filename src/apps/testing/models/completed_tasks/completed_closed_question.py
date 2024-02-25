from django.db import models

from apps.testing.abstractions.abstract_models.abstract_answer_options import AbstractClosedQuestionAnswerOption
from apps.testing.abstractions.abstract_models.abstract_tasks import AbstractClosedQuestion
from apps.testing.constants import APP_NAME
from apps.testing.models.completed_testing import CompletedTesting


class CompletedClosedQuestion(AbstractClosedQuestion):
    completed_testing = models.ForeignKey(
        CompletedTesting,
        on_delete=models.CASCADE,
        related_name='completed_closed_question_set',
        verbose_name='Завершённое тестирование'
    )


class ClosedQuestionAnswerOptionStudent(AbstractClosedQuestionAnswerOption):
    completed_closed_question = models.ForeignKey(
        CompletedClosedQuestion,
        on_delete=models.CASCADE,
        related_name='closed_question_answer_option_student_set',
        verbose_name='Закрытый вопрос'
    )

    class Meta(AbstractClosedQuestionAnswerOption.Meta):
        db_table = f'{APP_NAME}_closedQuestion_answerOption_student'


class ClosedQuestionAnswerOptionCorrect(AbstractClosedQuestionAnswerOption):
    closed_question_answer_option_student = models.OneToOneField(
        ClosedQuestionAnswerOptionStudent,
        on_delete=models.CASCADE,
        related_name='closed_question_answer_option_correct_set',
        verbose_name='Закрытый вопрос вариант ответа студента',
        primary_key=True
    )

    class Meta(AbstractClosedQuestionAnswerOption.Meta):
        db_table = f'{APP_NAME}_closedQuestion_answerOption_correct'
