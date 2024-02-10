from typing import Mapping, Sequence

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.views.generic import DetailView

from apps.testing.models import Testing
from apps.testing.constants import APP_NAME
from apps.testing.services import TaskService
from apps.testing.services.task_service import update_tasks_serial_number
from apps.testing.types import TaskType
from mixins import URLMixin


class TestingDetailView(URLMixin, LoginRequiredMixin, DetailView):
    model = Testing
    APP_NAME = APP_NAME

    @staticmethod
    def post(request: WSGIRequest, *args, **kwargs) -> redirect:
        update_tasks_serial_number(tasks_data=request.POST)
        return redirect('testing:testing_detail', pk=kwargs['pk'])

    def get_context_data(self, **kwargs) -> Mapping:
        context = super().get_context_data(**kwargs)
        task_service = TaskService(testing_pk=self.kwargs['pk'])
        sorted_tasks = task_service.sort_tasks_serial_number()
        is_teacher = self.request.user.is_teacher
        if is_teacher:
            context |= self._get_task_context_data(sorted_tasks)
        else:
            context |= self._get_pagination_context_data(sorted_tasks)
        return context

    def _get_task_context_data(self, sorted_tasks: Sequence[QuerySet]) -> Mapping[str, Mapping | Sequence[QuerySet]]:
        context = {}
        context |= self.get_testing_update_url_data() | self.get_testing_delete_url_data()
        tasks = [
            TaskType(name='Закрытый вопрос', url='task_closed_question_create'),
            TaskType(name='Открытый вопрос', url='task_open_question_create'),
            TaskType(name='Установление последовательности', url='task_sequencing_create'),
            TaskType(name='Установление соответствия', url='task_establishing_accordance_create'),
        ]
        context['task_data'] = {}
        for task in tasks:
            context['task_data'][task.name] = f'{APP_NAME}:{task.url}'
        context['tasks'] = sorted_tasks
        return context

    def _get_pagination_context_data(self, sorted_tasks: Sequence[QuerySet]) -> Mapping:
        paginator = Paginator(sorted_tasks, 1)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return {
            'paginator': paginator,
            'page_obj': page_obj,
            'task': page_obj.object_list[0]
        }
