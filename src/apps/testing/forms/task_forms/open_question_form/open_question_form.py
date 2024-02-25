from apps.testing.abstractions.abstract_forms import AbstractTaskForm
from apps.testing.models.tasks import OpenQuestion


class OpenQuestionForm(AbstractTaskForm):
    class Meta(AbstractTaskForm.Meta):
        model = OpenQuestion
