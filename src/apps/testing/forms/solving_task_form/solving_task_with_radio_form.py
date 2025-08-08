from django import forms

from apps.testing.forms.solving_task_form import SolvingTaskForm


class SolvingTaskWithRadioForm(SolvingTaskForm):
    answer = forms.ChoiceField(
        label='Варианты ответов',
        widget=forms.RadioSelect()
    )

    class Meta(SolvingTaskForm.Meta):
        pass
