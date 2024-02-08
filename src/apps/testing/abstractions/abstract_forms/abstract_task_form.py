from django import forms

from abstractions.abstract_form_fields import AbstractFormFieldDescription


class AbstractTaskForm(AbstractFormFieldDescription):
    class Meta:
        widgets = {
            'serial_number': forms.HiddenInput(),
            'testing': forms.HiddenInput()
        }
        exclude = ['type', ]
