from django import forms

from abstractions.abstract_form_fields import AbstractFormFieldDescription
from apps.testing.models import Task


class TaskForm(AbstractFormFieldDescription):
    class Meta:
        model = Task
        widgets = {
            'lead_time': forms.TimeInput(attrs={
                'class': 'uk-input uk-width-small',
                'type': 'time'
            }),
        }
        exclude = ['serial_number', 'type', 'testing']
