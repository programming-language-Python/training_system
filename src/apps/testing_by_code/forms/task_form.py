from django import forms

from abstractions.abstract_form_fields import AbstractFormFieldDescription
from apps.testing_by_code.models import Task


class TaskForm(AbstractFormFieldDescription):
    class Meta:
        model = Task
        widgets = {
            'weight': forms.NumberInput(attrs={
                'class': 'uk-input uk-form-width-small uk-form-small',
                'min': 1,
                'value': 1
            }),
            'lead_time': forms.TimeInput(attrs={
                'class': 'uk-input uk-width-small',
                'type': 'time'
            }),
        }
        fields = ('weight', 'lead_time', 'description',)
