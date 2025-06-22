from typing import Type

from apps.testing.abstractions.abstract_services import AbstractTaskService
from apps.testing.forms.solving_task_form import SolvingTaskForm


class OpenQuestionService(AbstractTaskService):
    def get_score(self, answer: str) -> int:
        is_correct_answer = self.task.open_question_answer_option_set.filter(
            correct_answer=answer
        ).exists()
        return 1 if is_correct_answer else 0

    def get_solving_form(self, solving_testing_pk: int):
        return self.initialize_solving_form(form=SolvingTaskForm, solving_testing_pk=solving_testing_pk)

    def initialize_solving_form(self, form, solving_testing_pk: int) -> Type[SolvingTaskForm]:
        student_answer = self.task.solving_task_set.get(solving_testing__pk=solving_testing_pk).answer
        if student_answer:
            form.base_fields['answer'].initial = student_answer.replace('"', '')
        return form
