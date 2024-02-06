from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import DetailView

from apps.testing.models import Testing, ClosedQuestion, OpenQuestion
from apps.testing.constants import APP_NAME
from apps.testing.services import TaskService
from apps.testing.types import TaskType
from mixins import URLMixin


class TestingDetailView(URLMixin, LoginRequiredMixin, DetailView):
    model = Testing
    APP_NAME = APP_NAME

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_service = TaskService(testing_pk=self.kwargs['pk'], )

        search_models = [ClosedQuestion, OpenQuestion]
        tasks = []
        for model in search_models:
            task = model.objects.filter(testing=self.kwargs['pk'])
            tasks.append(task)
        sorted_tasks = sorted(chain(*tasks), key=lambda data: data.serial_number)

        is_teacher_ = self.request.user.is_teacher
        if is_teacher_:
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
        else:
            paginator = Paginator(sorted_tasks, 1)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['paginator'] = paginator
            context['page_obj'] = page_obj
            context['task'] = page_obj.object_list[0]
        return context
