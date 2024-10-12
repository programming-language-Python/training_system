from django import forms

from apps.testing.abstractions.abstract_forms.abstract_task_form import AbstractTaskForm
from apps.testing.models.tasks import ClosedQuestion


class ClosedQuestionForm(AbstractTaskForm):
    task_name = forms.CharField(initial='closed_question', widget=forms.HiddenInput())

    class Meta(AbstractTaskForm.Meta):
        checkbox_input = forms.CheckboxInput(attrs={
            'class': 'uk-checkbox'
        })
        widgets = AbstractTaskForm.Meta.widgets | {
            'is_several_correct_answers': checkbox_input,
            'is_random_order_answer_options': checkbox_input,
            'is_partially_correct_execution': checkbox_input,
        }
        model = ClosedQuestion
