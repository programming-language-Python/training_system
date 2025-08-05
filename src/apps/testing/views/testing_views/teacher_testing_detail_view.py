from typing import Mapping

from django.db.models import QuerySet
from django.views.generic import DetailView

from apps.testing.models import Testing
from apps.testing.constants import APP_NAME
from apps.testing.types import TaskType
from mixins import ContextMixin, LoginMixin


class TeacherTestingDetailView(LoginMixin, ContextMixin, DetailView):
    template_name = 'testing/teacher_testing_detail.html'
    model = Testing
    APP_NAME = APP_NAME

    object = None

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
