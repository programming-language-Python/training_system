from typing import Mapping, Sequence

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.views.generic import DetailView

from apps.testing.models import Testing
from apps.testing.constants import APP_NAME
from apps.testing.services import TaskService
from apps.testing.services.task_service import update_tasks_serial_number
from apps.testing.types import TaskType
from mixins import URLMixin


class TestingDetailTeacherView(URLMixin, LoginRequiredMixin, DetailView):
    template_name = 'testing/testing_detail_teacher.html'
    model = Testing
    APP_NAME = APP_NAME

    object = None

    @staticmethod
    def post(request: WSGIRequest, *args, **kwargs) -> redirect:
        update_tasks_serial_number(tasks_data=request.POST)
        return redirect('testing:testing_detail', pk=kwargs['pk'])

    #
    def get_context_data(self, *args, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)
        task_service = TaskService(testing_pk=self.kwargs['pk'])
        sorted_tasks = task_service.sort_tasks_serial_number()
        context |= self._get_task_context_data(sorted_tasks)
        return context

    def _get_task_context_data(self, sorted_tasks: Sequence[QuerySet]) -> Mapping[str, Mapping | Sequence[QuerySet]]:
        context = {}
        context |= self.get_testing_update_url_data() | self.get_testing_delete_url_data()
        tasks = [
            TaskType(name='Закрытый вопрос', url='task_closed_question_create'),
            TaskType(name='Открытый вопрос', url='task_open_question_create'),
            # TaskType(name='Установление последовательности', url='task_sequencing_create'),
            # TaskType(name='Установление соответствия', url='task_establishing_accordance_create'),
        ]
        context['task_data'] = {}
        for task in tasks:
            context['task_data'][task.name] = f'{APP_NAME}:{task.url}'
        context['tasks'] = sorted_tasks
        context['quantity_task'] = len(sorted_tasks)
        return context
