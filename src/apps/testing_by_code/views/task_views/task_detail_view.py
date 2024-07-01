from django.views.generic import DetailView

from apps.testing_by_code.models import Task


class TaskDetailView(DetailView):
    model = Task
    template_name = 'testing_by_code/inc/task/_teacher_task_detail.html'
