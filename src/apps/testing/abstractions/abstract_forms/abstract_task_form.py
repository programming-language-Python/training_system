from django import forms

from abstractions.abstract_form_fields import AbstractFormFieldDescription


class AbstractTaskForm(AbstractFormFieldDescription):
    class Meta:
        widgets = {
            'lead_time': forms.TimeInput(attrs={
                'class': 'uk-input uk-width-small',
                'type': 'time'
            }),
            'serial_number': forms.HiddenInput(),
            'testing': forms.HiddenInput()
        }
        exclude = ['task_type', ]
