from django import forms

from apps.testing.forms.solving_task_form import SolvingTaskWithChoiceForm


class SolvingSequencingForm(SolvingTaskWithChoiceForm):
    template_name = 'testing/task/sequencing/solving_sequencing_form.html'
    answer = forms.MultipleChoiceField(
        label='Варианты ответов',
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )
