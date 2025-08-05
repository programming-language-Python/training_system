from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect

from apps.testing_by_code.models import Task
from services import update_serial_number_tasks


def update_serial_number_tasks_view(request: WSGIRequest, pk: int):
    update_serial_number_tasks(task=Task, tasks_data=request.POST)
    return redirect('testing_by_code:testing_detail', pk=pk)
