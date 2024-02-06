from itertools import chain
from typing import Mapping, Sequence, MutableMapping

from django.core.paginator import Paginator
from django.db.models import QuerySet

from apps.testing.models import ClosedQuestion, OpenQuestion


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
