from django import forms

from abstractions.abstract_form_fields import AbstractFormFieldDescription


class AbstractAnswerOptionWithCheckboxForm(AbstractFormFieldDescription):
    class Meta:
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
