from django import forms

from apps.testing.abstractions.abstract_forms.abstract_task_form import AbstractTaskForm
from apps.testing.models import ClosedQuestion


class ClosedQuestionForm(AbstractTaskForm):
    closed_question_meta = ClosedQuestion._meta
    is_several_correct_answers = forms.BooleanField(
        label=closed_question_meta.get_field('is_several_correct_answers').verbose_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox'
            }
        )
    )
    is_random_order_answer_options = forms.BooleanField(
        label=closed_question_meta.get_field('is_random_order_answer_options').verbose_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox'
            }
        )
    )
    is_partially_correct_execution = forms.BooleanField(
        label=closed_question_meta.get_field('is_partially_correct_execution').verbose_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox'
            }
        )
    )

    class Meta(AbstractTaskForm.Meta):
        model = ClosedQuestion
