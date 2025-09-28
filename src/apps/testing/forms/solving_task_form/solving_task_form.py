from abstractions.abstract_forms import AbstractSolvingTaskForm
from apps.testing.models import SolvingTask


class SolvingTaskForm(AbstractSolvingTaskForm):
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.score = instance.task.service.get_score(self.cleaned_data['answer'])
        instance.save()
        return instance

    class Meta(AbstractSolvingTaskForm.Meta):
        model = SolvingTask
