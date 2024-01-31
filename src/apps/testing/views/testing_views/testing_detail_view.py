from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from apps.testing.models import Testing
from apps.testing.constants import APP_NAME
from apps.testing.types import TaskType
from mixins import URLMixin


class TestingDetailView(URLMixin, LoginRequiredMixin, DetailView):
    model = Testing
    APP_NAME = APP_NAME

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        return context
