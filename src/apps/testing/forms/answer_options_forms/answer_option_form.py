from django import forms

from abstractions.abstract_form_fields import AbstractFormFieldDescription
from apps.testing.models.task_answer_options import AnswerOption


class AnswerOptionForm(AbstractFormFieldDescription):
    class Meta:
        model = AnswerOption
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
        fields = ('serial_number', 'description', 'is_correct',)
