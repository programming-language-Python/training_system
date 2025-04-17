from typing import Type

from django.utils.html import strip_tags

from apps.testing.abstractions.abstract_services import AbstractTaskService
from apps.testing.forms.solving_task_form import SolvingTaskForm


class AbstractTaskWithChoiceService(AbstractTaskService):
    def initialize_solving_form(self, form, solving_testing_pk: int) -> Type[SolvingTaskForm]:
        student_answer = self.task.solving_task_set.get(solving_testing__pk=solving_testing_pk).answer
        if student_answer:
            form.base_fields['answer'].initial = student_answer
        return form

    def _get_answer_field_choices(self):
        return set((answer_option.id, strip_tags(answer_option.description)) for answer_option in self._answer_options)

    @property
    def _answer_options(self):
        raise NotImplementedError('Не реализован метод _answer_options')
