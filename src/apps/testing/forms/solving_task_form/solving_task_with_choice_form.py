from django import forms

from apps.testing.forms.solving_task_form import SolvingTaskForm


class SolvingTaskWithChoiceForm(SolvingTaskForm):
    answer = forms.MultipleChoiceField(
        label='Варианты ответов',
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta(SolvingTaskForm.Meta):
        pass
