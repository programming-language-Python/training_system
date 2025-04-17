from typing import Mapping

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.views.generic import DetailView

from apps.testing.models import Testing
from apps.testing.constants import APP_NAME
from apps.testing.services.task_service import update_tasks_serial_number
from apps.testing.types import TaskType
from mixins import ContextMixin, LoginMixin


class TeacherTestingDetailView(LoginMixin, ContextMixin, DetailView):
    template_name = 'testing/teacher_testing_detail.html'
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

    def _get_task_context_data(self) -> Mapping[str, Mapping | QuerySet | int]:
        tasks = self.object.task_set.all()
        context = {
            'tasks': tasks,
            'quantity_task': tasks.count(),
            'tasks_types': list(TaskType)
        }
        return context
