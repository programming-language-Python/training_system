from typing import Type

from django.db.models import Model
from django.http import QueryDict


def update_serial_number_tasks(task: Type['Model'], tasks_data: QueryDict) -> None:
    task_pks = tasks_data.getlist('pk')
    serial_numbers = tasks_data.getlist('serial-number')
    tasks = zip(task_pks, serial_numbers)
    for pk, serial_number in tasks:
        task.objects.filter(pk=pk).update(serial_number=serial_number)
