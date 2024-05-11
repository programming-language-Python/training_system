from itertools import chain
from typing import Mapping, Sequence

from django.apps import apps
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import QueryDict

from apps.testing.constants import APP_NAME
from apps.testing.forms.task_forms.open_question_form import OpenQuestionAnswerForm
from apps.testing.models import SolvingTesting
from apps.testing.models.solving_tasks import SolvingOpenQuestion
from apps.testing.models.tasks import ClosedQuestion, OpenQuestion
from apps.user.models import Student


def update_tasks_serial_number(tasks_data: QueryDict) -> None:
    class_names = tasks_data.getlist('class-name')
    task_pks = tasks_data.getlist('pk')
    serial_numbers = tasks_data.getlist('serial-number')
    tasks = zip(class_names, task_pks, serial_numbers)
    for class_name, pk, serial_number in tasks:
        model = apps.get_model(app_label=APP_NAME, model_name=class_name)
        model.objects.filter(pk=pk).update(serial_number=serial_number)


class TaskService:
    testing_pk: int

    def __init__(self, testing_pk: int) -> None:
        self.testing_pk = testing_pk

    def set_initial_values_form_fields(self, fields: Mapping) -> Mapping:
        if fields.get('serial_number'):
            fields['serial_number'].initial = self.get_quantity() + 1
        fields['testing'].initial = self.testing_pk
        return fields

    def get_quantity(self) -> int:
        return len(self.sort_tasks_serial_number())

    def get_pagination_context(self, page_number: int) -> Mapping:
        paginator = Paginator(self.sort_tasks_serial_number, 1)
        page_obj = paginator.get_page(page_number)
        pagination_context = {
            'paginator': paginator,
            'page_obj': page_obj,
            'task': page_obj.object_list[0]
        }
        return pagination_context

    def sort_tasks_serial_number(self) -> Sequence[QuerySet]:
        search_models = [ClosedQuestion, OpenQuestion]
        tasks = []
        for model in search_models:
            task = model.objects.filter(testing=self.testing_pk)
            tasks.append(task)
        sorted_tasks = sorted(chain(*tasks), key=lambda data: data.serial_number)
        return sorted_tasks
