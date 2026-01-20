from typing import Type

from django.utils.html import strip_tags

from apps.testing.abstractions.abstract_services import AbstractTaskService
from apps.testing.forms.solving_task_form import SolvingTaskForm


class AbstractTaskWithChoiceService(AbstractTaskService):
    def __init__(self, task):
        super().__init__(task)
        self.solving_task = None

    def initialize_solving_form(self, solving_testing_pk: int) -> Type[SolvingTaskForm]:
        self.solving_task = self.task.solving_task_set.get(solving_testing__pk=solving_testing_pk)
        form = self.solving_form(initial={
            'answer': self.solving_task.answer,
            'time_left': self.solving_task.time_left,
        })
        answer_field_choices = self._get_answer_field_choices
        form.base_fields['answer'].choices = answer_field_choices
        form.fields['answer'].choices = answer_field_choices
        return form

    @property
    def _get_answer_field_choices(self):
        answer_options = self._answer_options
        return set((answer_option.id, strip_tags(answer_option.description)) for answer_option in answer_options)

    @property
    def _answer_options(self):
        raise NotImplementedError('Не реализован метод _answer_options')
