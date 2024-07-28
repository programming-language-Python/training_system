from typing import Mapping, Sequence

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.views.generic import DetailView

from apps.testing.models import Testing
from apps.testing.constants import APP_NAME
from apps.testing.models.tasks import TaskType
from apps.testing.services import TaskService
from apps.testing.services.task_service import update_tasks_serial_number
from mixins import ContextMixin


class TestingDetailTeacherView(ContextMixin, LoginRequiredMixin, DetailView):
    template_name = 'testing/testing_detail_teacher.html'
    model = Testing
    APP_NAME = APP_NAME

    object = None

    @staticmethod
    def post(request: WSGIRequest, *args, **kwargs) -> redirect:
        update_tasks_serial_number(tasks_data=request.POST)
        return redirect('testing:testing_detail', pk=kwargs['pk'])

    def get_context_data(self, *args, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)
        context |= self.get_testing_detail_data(
            is_solving_testing=self.object.testing_solving_testing_set.exists(),
        )
        context |= self._get_task_context_data()
        return context

    def _get_task_context_data(self) -> Mapping[str, Mapping | Sequence[QuerySet]]:
        task_service = TaskService(testing_pk=self.kwargs['pk'])
        sorted_tasks = task_service.sort_tasks_serial_number()
        context = {
            'task_data': {},
            'tasks': sorted_tasks,
            'quantity_task': len(sorted_tasks),
            'tasks_types': TaskType.objects.all()
        }
        return context
