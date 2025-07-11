from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect

from apps.testing_by_code.services.task_service import update_tasks_serial_number


def update_tasks_serial_number_view(request: WSGIRequest, pk: int):
    update_tasks_serial_number(tasks_data=request.POST)
    return redirect('testing_by_code:testing_detail', pk=pk)
