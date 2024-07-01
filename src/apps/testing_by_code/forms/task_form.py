from abstractions.abstract_forms import AbstractTaskForm
from apps.testing_by_code.models import Task


class TaskForm(AbstractTaskForm):
    class Meta:
        model = Task
        fields = ('weight',)
