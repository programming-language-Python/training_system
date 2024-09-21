from django import forms

from abstractions.abstract_form_fields import AbstractFormFieldDescription
from apps.testing.models.task_answer_options import ClosedQuestionAnswerOption


class ClosedQuestionAnswerOptionForm(AbstractFormFieldDescription):
    answer_option_meta = ClosedQuestionAnswerOption._meta

    class Meta:
        model = ClosedQuestionAnswerOption
        widgets = {
            'serial_number': forms.NumberInput(attrs={
                'class': 'serial-number',
                'data-name': 'serial-number',
                'data-is-fit-block-to-content-size': 'True',
                'min': 1
            }),
            'is_correct': forms.CheckboxInput(attrs={
                'class': 'uk-checkbox',
                'data-name': 'is-correct',
            })
        }
        fields = ('serial_number', 'description', 'is_correct', 'closed_question',)
