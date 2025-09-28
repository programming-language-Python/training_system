from abstractions.abstract_forms import AbstractSolvingTaskForm
from apps.testing_by_code.models import SolvingTask


class SolvingTaskForm(AbstractSolvingTaskForm):
    class Meta(AbstractSolvingTaskForm.Meta):
        model = SolvingTask
