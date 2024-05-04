from django import forms

from abstractions.abstract_form_fields import AbstractFormFieldDescription


class AbstractTaskForm(AbstractFormFieldDescription):
    lead_time = forms.TimeField(
        label='Время выполнения',
        required=False,
        widget=forms.TimeInput(
            attrs={
                'class': 'uk-input uk-width-small',
                'type': 'time'
            }
        )
    )

    class Meta:
        widgets = {
            'serial_number': forms.HiddenInput(),
            'testing': forms.HiddenInput()
        }
        exclude = ['task_type', ]
