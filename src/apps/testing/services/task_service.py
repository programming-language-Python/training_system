from typing import Mapping, Type, Iterable

from django.apps import apps
from django.forms import inlineformset_factory, ModelForm
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags

from apps.testing.constants import APP_NAME
from apps.testing.interfaces import ITaskService
from apps.testing.models import Testing, Task, SolvingTask
from apps.testing.services import ClosedQuestionService, OpenQuestionService
from apps.testing.services.closed_question_service import closed_question_set_answer
from apps.testing.services.open_question_service import open_question_set_answer
from apps.testing.types import ValidTask, InlineFormSetFactory, TaskType, Id


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
    def _create_task(valid_task: ValidTask) -> Task:
        testing = get_object_or_404(Testing, pk=valid_task.testing_pk)
        task = valid_task.task_forms.form.save(commit=False)
        task.serial_number = testing.task_set.count() + 1
        task.type = valid_task.type
        task.testing = testing
        task.save()
        return task

    @staticmethod
    def _create_answer_option_set(task: Task, answer_option_form_set: Type[inlineformset_factory]) -> None:
        answer_option_form_set.instance = task
        answer_option_form_set.save()

    @staticmethod
    def _create_additional_fields(task: Task, additional_form: ModelForm) -> None:
        additional_model = additional_form.save(commit=False)
        additional_model.task = task
        additional_model.save()

    def update(self, task_forms: InlineFormSetFactory) -> None:
        task = task_forms.form.save()
        task_forms.form_set.save()
        if task_forms.additional_form:
            self._update_additional_model(
                task=task,
                cleaned_data=task_forms.additional_form.cleaned_data
            )

    @staticmethod
    def _update_additional_model(task: Task, cleaned_data: Mapping) -> None:
        match task.task_type:
            case TaskType.CLOSED_QUESTION:
                task_service = ClosedQuestionService(task)
        task_service.update(cleaned_data)

    @staticmethod
    def get_answer_field_choices(task_service: ITaskService):
        answer_options = task_service.get_answer_options()
        ids = answer_options.values_list('id', flat=True)
        descriptions = map(strip_tags, answer_options.values_list('description', flat=True))
        return set(zip(ids, descriptions))

    @staticmethod
    def get_weight(task: Task, answer: str | Iterable[Id]) -> int:
        match task.task_type:
            case TaskType.CLOSED_QUESTION:
                task_service = ClosedQuestionService(task)
            case TaskType.OPEN_QUESTION:
                task_service = OpenQuestionService(task)
        return task_service.get_weight(answer)

    @staticmethod
    def set_answer(solving_task: SolvingTask, answer: str | Iterable[Id]) -> None:
        match solving_task.task.task_type:
            case TaskType.CLOSED_QUESTION:
                closed_question_set_answer(solving_task, answer)
            case TaskType.OPEN_QUESTION:
                open_question_set_answer(solving_task, answer)
