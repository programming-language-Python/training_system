from django import forms

from abstractions.abstract_form_fields import AbstractFormFieldDescription
from apps.testing.models.task_answer_options import ClosedQuestionAnswerOption


class ClosedQuestionAnswerOptionForm(AbstractFormFieldDescription):
    answer_option_meta = ClosedQuestionAnswerOption._meta
    serial_number = forms.IntegerField(
        label=answer_option_meta.get_field('serial_number').verbose_name,
        widget=forms.NumberInput(
            attrs={
                'class': 'serial-number',
                'data-name': 'serial-number',
                'data-is-fit-block-to-content-size': 'True',
                'min': 1
            }
        )
    )
    is_correct = forms.BooleanField(
        label=answer_option_meta.get_field('is_correct').verbose_name,
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'uk-checkbox',
                'data-name': 'is-correct',
            }
        )
    )

    class Meta:
        model = ClosedQuestionAnswerOption
        fields = ('serial_number', 'description', 'is_correct', 'closed_question',)
