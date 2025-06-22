from typing import Type, Iterable

from django.apps import apps
from django.forms import inlineformset_factory, ModelForm
from django.http import QueryDict
from django.shortcuts import get_object_or_404

from apps.testing.constants import APP_NAME
from apps.testing.models import Testing, SolvingTask
from apps.testing.types import ValidTask, Id
from custom_types import InlineFormSetFactory


def update_tasks_serial_number(tasks_data: QueryDict) -> None:
    class_names = tasks_data.getlist('class-name')
    task_pks = tasks_data.getlist('pk')
    serial_numbers = tasks_data.getlist('serial-number')
    tasks = zip(class_names, task_pks, serial_numbers)
    for class_name, pk, serial_number in tasks:
        model = apps.get_model(app_label=APP_NAME, model_name=class_name)
        model.objects.filter(pk=pk).update(serial_number=serial_number)


class TaskService:
    def create(self, valid_task: ValidTask) -> None:
        task = self._create_task(valid_task)
        task_forms = valid_task.task_forms
        self._create_answer_option_set(task, answer_option_form_set=task_forms.form_set)
        additional_form = task_forms.additional_form
        if additional_form:
            self._create_additional_fields(task, additional_form)

    @staticmethod
    def _create_task(valid_task: ValidTask):
        testing = get_object_or_404(Testing, pk=valid_task.testing_pk)
        task = valid_task.task_forms.form.save(commit=False)
        task.serial_number = testing.task_set.count() + 1
        task.type = valid_task.type
        task.testing = testing
        task.save()
        return task

    @staticmethod
    def _create_answer_option_set(task, answer_option_form_set: Type[inlineformset_factory]) -> None:
        answer_option_form_set.instance = task
        answer_option_form_set.save()

    @staticmethod
    def _create_additional_fields(task, additional_form: ModelForm) -> None:
        additional_model = additional_form.save(commit=False)
        additional_model.task = task
        additional_model.save()

    @staticmethod
    def update(task_forms: InlineFormSetFactory) -> None:
        task = task_forms.form.save()
        task_forms.form_set.save()
        try:
            task.service.update(cleaned_data=task_forms.additional_form.cleaned_data)
        except AttributeError:
            pass

    @staticmethod
    def save_answer(solving_task: SolvingTask, answer: str | Iterable[Id]) -> None:
        solving_task.answer = answer
        solving_task.score = solving_task.task.service.get_score(answer)
        solving_task.save()
